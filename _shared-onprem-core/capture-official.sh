#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

mkdir -p captures_official

docker run --rm \
  --network host \
  --add-host official.local:127.0.0.1 \
  -v "${ROOT_DIR}":/work \
  -w /work \
  mcr.microsoft.com/playwright:v1.58.2-jammy \
  bash -lc "cd /tmp && npm init -y >/dev/null 2>&1 && npm install playwright@1.58.2 >/dev/null 2>&1 && NODE_PATH=/tmp/node_modules node /work/scripts/capture-official-ui.js"

echo "[done] Official captures saved in ./captures_official"
