#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="${PLAYWRIGHT_IMAGE:-mcr.microsoft.com/playwright:v1.58.2-jammy}"

cd "${ROOT_DIR}"

docker run --rm \
  --network host \
  -v "${ROOT_DIR}":/work \
  -w /work \
  "${IMAGE}" \
  bash -lc "./scripts/capture-ui-in-container.sh"

echo "[done] Screenshots are saved under ./captures"
