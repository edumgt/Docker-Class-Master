#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

PROJECT_NAME="${PROJECT_NAME:-official-ui}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.official-ui.yml}"

if [[ "${1:-}" == "--volumes" ]]; then
  docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" down --remove-orphans --volumes
else
  docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" down --remove-orphans
fi

echo "[stopped] official UI compose is down"
