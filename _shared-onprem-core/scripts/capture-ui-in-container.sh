#!/usr/bin/env bash
set -euo pipefail

mkdir -p captures

targets=(
  "odoo 9000"
  "erpnext 9001"
  "zulip 9002"
  "taiga 9003"
  "tryton 9004"
)

for item in "${targets[@]}"; do
  sol="${item%% *}"
  port="${item##* }"
  user="${sol}_member1"
  base="http://127.0.0.1:${port}"
  out="captures/${sol}"

  mkdir -p "${out}"

  echo "[capture] ${sol} runtime"
  npx -y playwright@1.58.2 screenshot --device='Desktop Chrome' "${base}/app-ui" "${out}/01-runtime.png"

  echo "[capture] ${sol} login"
  npx -y playwright@1.58.2 screenshot --device='Desktop Chrome' "${base}/login-ui" "${out}/02-login.png"

  echo "[login-api] ${sol}"
  curl -sS -X POST "${base}/login" \
    -H 'Content-Type: application/json' \
    -d "{\"username\":\"${user}\",\"password\":\"123456\"}" >/tmp/login-${sol}.json

  echo "[capture] ${sol} dashboard"
  npx -y playwright@1.58.2 screenshot --device='Desktop Chrome' "${base}/dashboard-ui?username=${user}" "${out}/03-dashboard.png"
done

python3 - <<'PY'
import json
from datetime import datetime, timezone
from pathlib import Path

solutions = ["odoo", "erpnext", "zulip", "taiga", "tryton"]
summary = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "solutions": [],
}
for s in solutions:
    summary["solutions"].append(
        {
            "solution": s,
            "runtime": f"captures/{s}/01-runtime.png",
            "login": f"captures/{s}/02-login.png",
            "dashboard": f"captures/{s}/03-dashboard.png",
        }
    )

Path("captures/summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print("[done] captures/summary.json")
PY
