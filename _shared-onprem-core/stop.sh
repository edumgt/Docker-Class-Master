#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

if [[ "${1:-}" == "--volumes" ]]; then
  docker compose down --remove-orphans --volumes
else
  docker compose down --remove-orphans
fi

echo "[stopped] docker compose down complete"
