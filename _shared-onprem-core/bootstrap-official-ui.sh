#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

wait_for_container() {
  local container="$1"
  local timeout="${2:-300}"
  local elapsed=0
  local status

  while (( elapsed < timeout )); do
    status="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "${container}" 2>/dev/null || true)"
    if [[ "${status}" == "healthy" || "${status}" == "running" ]]; then
      return 0
    fi
    sleep 2
    elapsed=$((elapsed + 2))
  done

  echo "[error] ${container} did not become ready in ${timeout}s"
  return 1
}

wait_for_http() {
  local url="$1"
  local timeout="${2:-300}"
  local elapsed=0
  local code

  while (( elapsed < timeout )); do
    code="$(docker run --rm --network host curlimages/curl:8.8.0 -sS -o /dev/null -w '%{http_code}' "${url}" 2>/dev/null || true)"
    if [[ -n "${code}" && "${code}" != "000" ]]; then
      return 0
    fi
    sleep 2
    elapsed=$((elapsed + 2))
  done

  echo "[error] ${url} did not become reachable in ${timeout}s"
  return 1
}

echo "[wait] core containers"
wait_for_container odoo-official-rdbms
wait_for_container odoo-official-web
wait_for_container erpnext-official-rdbms
wait_for_container erpnext-official-web
wait_for_container tryton-official-rdbms
wait_for_container tryton-official-web
wait_for_container zulip-official-rdbms
wait_for_container zulip-official-rabbitmq
wait_for_container zulip-official-redis
wait_for_container zulip-official-web

echo "[bootstrap] odoo"
odoo_db_exists="$(docker exec odoo-official-rdbms psql -U odoo -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='odoo_official'" | tr -d '[:space:]')"
if [[ "${odoo_db_exists}" != "1" ]]; then
  docker exec odoo-official-web odoo \
    -d odoo_official \
    --db_host=odoo-official-rdbms \
    --db_port=5432 \
    --db_user=odoo \
    --db_password=123456 \
    -i base \
    --without-demo=all \
    --stop-after-init
  docker restart odoo-official-web >/dev/null
fi

echo "[bootstrap] erpnext"
if ! docker exec erpnext-official-web bash -lc "[ -f /home/frappe/frappe-bench/sites/official.local/site_config.json ]"; then
  docker exec erpnext-official-web bash -lc "bench new-site official.local --db-root-username root --db-root-password 123456 --admin-password 123456 --db-password 123456 --db-host erpnext-official-rdbms --set-default --install-app erpnext"
fi
docker exec erpnext-official-web bash -lc "bench use official.local >/dev/null 2>&1 || true"
docker exec erpnext-official-web bash -lc "bench --site official.local set-config db_host erpnext-official-rdbms >/dev/null 2>&1 || true"
docker exec erpnext-official-web bash -lc "bench --site official.local set-config db_password 123456 >/dev/null 2>&1 || true"
erpnext_db_name="$(docker exec erpnext-official-web bash -lc "python3 - <<'PY'
import json
from pathlib import Path
cfg_path = Path('/home/frappe/frappe-bench/sites/official.local/site_config.json')
cfg = json.loads(cfg_path.read_text())
print(cfg.get('db_name', ''))
PY" | tr -d '[:space:]')"
if [[ -n "${erpnext_db_name}" ]]; then
  docker exec erpnext-official-rdbms mariadb -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS \`${erpnext_db_name}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER IF NOT EXISTS '${erpnext_db_name}'@'%' IDENTIFIED BY '123456'; ALTER USER '${erpnext_db_name}'@'%' IDENTIFIED BY '123456'; GRANT ALL PRIVILEGES ON \`${erpnext_db_name}\`.* TO '${erpnext_db_name}'@'%'; FLUSH PRIVILEGES;"
fi

echo "[bootstrap] tryton"
tryton_db_exists="$(docker exec tryton-official-rdbms psql -U tryton -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='tryton_official'" | tr -d '[:space:]')"
if [[ "${tryton_db_exists}" != "1" ]]; then
  docker exec tryton-official-rdbms psql -U tryton -d postgres -c "CREATE DATABASE tryton_official OWNER tryton;"
fi
tryton_schema_ready="$(docker exec tryton-official-rdbms psql -U tryton -d tryton_official -tAc "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='res_user'" | tr -d '[:space:]')"
if [[ "${tryton_schema_ready}" != "1" ]]; then
  docker exec tryton-official-web bash -lc "echo 123456 >/tmp/tryton_pass && export TRYTONPASSFILE=/tmp/tryton_pass && export TRYTOND_DATABASE_URI='postgresql://tryton:123456@tryton-official-rdbms:5432/' && printf '\n' | trytond-admin -d tryton_official --all -p"
fi

echo "[bootstrap] zulip"
wait_for_http "http://127.0.0.1:9064/login/" 600
docker exec zulip-official-web bash -lc "echo 123456 >/home/zulip/zulip_pw && chown zulip:zulip /home/zulip/zulip_pw && chmod 600 /home/zulip/zulip_pw"
docker exec zulip-official-web bash -lc "su zulip -c '/home/zulip/deployments/current/manage.py create_realm --string-id= --password-file /home/zulip/zulip_pw --automated OfficialZulip admin@example.com AdminUser' || true"
docker exec -i zulip-official-web bash -lc "su zulip -c '/home/zulip/deployments/current/manage.py shell'" <<'PY'
from zerver.lib.create_user import create_user
from zerver.models import Realm, UserProfile

realm = Realm.objects.filter(string_id="").first()
if realm is None:
    raise SystemExit("Root realm was not created")

user = UserProfile.objects.filter(realm=realm, delivery_email="admin@example.com").first()
if user is None:
    user = UserProfile.objects.filter(realm=realm, email="admin@example.com").first()

if user is None:
    user = create_user(
        email="admin@example.com",
        password="123456",
        realm=realm,
        full_name="AdminUser",
        active=True,
        role=UserProfile.ROLE_REALM_OWNER,
    )

user.delivery_email = "admin@example.com"
user.set_password("123456")
user.is_active = True
user.role = UserProfile.ROLE_REALM_OWNER
user.save(update_fields=["delivery_email", "password", "is_active", "role"])

print(f"realm={realm.id} login_email={user.delivery_email} stored_email={user.email} role={user.role}")
PY

echo "[done] official UI bootstrap complete"
