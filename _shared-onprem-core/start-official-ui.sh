#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

PROJECT_NAME="${PROJECT_NAME:-official-ui}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.official-ui.yml}"

CONTAINERS=(
  odoo-official-rdbms
  odoo-official-web
  erpnext-official-rdbms
  erpnext-official-redis
  erpnext-official-web
  tryton-official-rdbms
  tryton-official-web
  taiga-official-front
  zulip-official-rdbms
  zulip-official-rabbitmq
  zulip-official-redis
  zulip-official-memcached
  zulip-official-web
)

docker rm -f "${CONTAINERS[@]}" >/dev/null 2>&1 || true

docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" up -d
./bootstrap-official-ui.sh

echo
docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" ps

echo
cat <<'MSG'
[official ui]
- odoo    : http://localhost:9060
- erpnext : http://localhost:9061 (Host: official.local)
- tryton  : http://localhost:9062
- taiga   : http://localhost:9063
- zulip   : http://localhost:9064

[default login]
- odoo    : admin / admin
- erpnext : Administrator / 123456
- tryton  : admin / 123456 (db: tryton_official)
- zulip   : admin@example.com / 123456
MSG
