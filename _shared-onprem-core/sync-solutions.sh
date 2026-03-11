#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOLUTIONS_DIR="${ROOT_DIR}/solutions"
GIT_TIMEOUT_SECONDS="${GIT_TIMEOUT_SECONDS:-10}"

mkdir -p "${SOLUTIONS_DIR}"

repos=(
  "odoo https://github.com/odoo/odoo.git"
  "erpnext https://github.com/frappe/erpnext.git"
  "zulip https://github.com/zulip/zulip.git"
  "taiga https://github.com/taigaio/taiga-docker.git"
  "tryton https://github.com/tryton/tryton.git"
)

echo "[sync] target: ${SOLUTIONS_DIR}"

for item in "${repos[@]}"; do
  name="${item%% *}"
  url="${item#* }"
  dir="${SOLUTIONS_DIR}/${name}"

  mkdir -p "${dir}"

  if [[ -d "${dir}/.git" ]]; then
    if git -C "${dir}" rev-parse --verify HEAD >/dev/null 2>&1; then
      echo "[pull] ${name}"
      timeout "${GIT_TIMEOUT_SECONDS}" git -C "${dir}" pull --ff-only || echo "[warn] pull failed: ${name}"
    else
      echo "[fetch] ${name} (no local commits yet)"
      timeout "${GIT_TIMEOUT_SECONDS}" git -C "${dir}" fetch --depth 1 origin || echo "[warn] fetch failed: ${name}"
    fi
  else
    if [[ -z "$(ls -A "${dir}")" ]]; then
      echo "[clone] ${name}"
      if timeout "${GIT_TIMEOUT_SECONDS}" git clone --depth 1 "${url}" "${dir}"; then
        echo "[ok] clone success: ${name}"
      else
        echo "[warn] clone failed: ${name}"
        git -C "${dir}" init >/dev/null 2>&1 || true
        git -C "${dir}" remote remove origin >/dev/null 2>&1 || true
        git -C "${dir}" remote add origin "${url}" >/dev/null 2>&1 || true
      fi
    else
      echo "[init] ${name} (non-empty placeholder folder)"
      git -C "${dir}" init >/dev/null 2>&1 || true
      git -C "${dir}" remote remove origin >/dev/null 2>&1 || true
      git -C "${dir}" remote add origin "${url}" >/dev/null 2>&1 || true
      echo "[ok] remote configured: ${name} -> ${url}"
    fi
  fi

done

echo "[done] sync finished"
