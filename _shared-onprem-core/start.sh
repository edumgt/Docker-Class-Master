#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

./sync-solutions.sh || true

export DOCKER_BUILDKIT="${DOCKER_BUILDKIT:-0}"
export COMPOSE_DOCKER_CLI_BUILD="${COMPOSE_DOCKER_CLI_BUILD:-0}"

docker compose up -d --build

echo
printf '%s\n' "[running]"
docker compose ps

echo
cat <<'MSG'
[access]
- odoo auth    : http://localhost:9000
- erpnext auth : http://localhost:9001
- zulip auth   : http://localhost:9002
- taiga auth   : http://localhost:9003
- tryton auth  : http://localhost:9004

[login example]
curl -s -X POST http://localhost:9000/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"odoo_member1","password":"123456"}'
MSG
