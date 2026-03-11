#!/usr/bin/env python3
import base64
import hashlib
import hmac
import html
import json
import os
import re
import subprocess
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

SOLUTION = os.getenv("SOLUTION", "solution")
PORT = int(os.getenv("PORT", "9000"))
JWT_SECRET = os.getenv("JWT_SECRET", "123456")
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "123456")
TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "2592000"))

DB_TYPE = os.getenv("DB_TYPE", "postgres")  # postgres | mariadb
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", SOLUTION)
DB_USER = os.getenv("DB_USER", SOLUTION)
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")

SEED_USERS = [
    f"{SOLUTION}_member1",
    f"{SOLUTION}_member2",
    f"{SOLUTION}_member3",
]

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,64}$")


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_jwt(username: str) -> str:
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": username,
        "solution": SOLUTION,
        "iat": now,
        "exp": now + TOKEN_TTL_SECONDS,
    }
    header_part = b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_part = b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_part}.{payload_part}"
    signature = hmac.new(
        JWT_SECRET.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256
    ).digest()
    return f"{signing_input}.{b64url(signature)}"


def is_valid_username(username: str) -> bool:
    return bool(USERNAME_PATTERN.fullmatch(username))


def run_sql(sql: str) -> str:
    if DB_TYPE == "postgres":
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD
        cmd = [
            "psql",
            "-h",
            DB_HOST,
            "-p",
            DB_PORT,
            "-U",
            DB_USER,
            "-d",
            DB_NAME,
            "-At",
            "-F",
            "\t",
            "-c",
            sql,
        ]
    elif DB_TYPE == "mariadb":
        cmd = [
            "mariadb",
            "-h",
            DB_HOST,
            "-P",
            DB_PORT,
            "-u",
            DB_USER,
            f"-p{DB_PASSWORD}",
            f"-D{DB_NAME}",
            "-N",
            "-B",
            "-e",
            sql,
        ]
        env = None
    else:
        raise RuntimeError(f"Unsupported DB_TYPE: {DB_TYPE}")

    cp = subprocess.run(
        cmd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return cp.stdout.strip()


def sql_esc(value: str) -> str:
    return value.replace("'", "''")


def seed_members() -> None:
    if DB_TYPE == "postgres":
        for username in SEED_USERS:
            token = make_jwt(username)
            sql = (
                "INSERT INTO members (username, password, jwt_token) "
                f"VALUES ('{sql_esc(username)}', '{sql_esc(DEFAULT_PASSWORD)}', '{sql_esc(token)}') "
                "ON CONFLICT (username) DO UPDATE SET "
                "password = EXCLUDED.password, jwt_token = EXCLUDED.jwt_token;"
            )
            run_sql(sql)
    elif DB_TYPE == "mariadb":
        for username in SEED_USERS:
            token = make_jwt(username)
            sql = (
                "INSERT INTO members (username, password, jwt_token) "
                f"VALUES ('{sql_esc(username)}', '{sql_esc(DEFAULT_PASSWORD)}', '{sql_esc(token)}') "
                "ON DUPLICATE KEY UPDATE "
                "password = VALUES(password), jwt_token = VALUES(jwt_token);"
            )
            run_sql(sql)


def count_members() -> int:
    out = run_sql("SELECT COUNT(*) FROM members;")
    return int(out.splitlines()[-1]) if out else 0


def list_members() -> list[dict]:
    out = run_sql("SELECT username, password, jwt_token FROM members ORDER BY username;")
    if not out:
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        rows.append(
            {
                "username": parts[0],
                "password": parts[1],
                "jwt_token": parts[2],
            }
        )
    return rows


def get_member(username: str) -> tuple[str, str] | None:
    safe = sql_esc(username)
    out = run_sql(f"SELECT username, password FROM members WHERE username = '{safe}' LIMIT 1;")
    if not out:
        return None
    line = out.splitlines()[0]
    parts = line.split("\t")
    if len(parts) < 2:
        return None
    return parts[0], parts[1]


def get_member_token(username: str) -> str:
    safe = sql_esc(username)
    out = run_sql(f"SELECT jwt_token FROM members WHERE username = '{safe}' LIMIT 1;")
    if not out:
        return ""
    return out.splitlines()[0]


def update_member_jwt(username: str, token: str) -> None:
    safe_user = sql_esc(username)
    safe_tok = sql_esc(token)
    run_sql(f"UPDATE members SET jwt_token = '{safe_tok}' WHERE username = '{safe_user}';")


def render_html(title: str, body: str) -> bytes:
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{ --bg:#f5f7fb; --card:#ffffff; --line:#d8e0ef; --ink:#0f1c33; --accent:#1f6feb; --ok:#1a7f37; --err:#b42318; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Segoe UI, Arial, sans-serif; background:linear-gradient(180deg,#eef3ff,#f9fbff); color:var(--ink); }}
    .wrap {{ max-width:900px; margin:32px auto; padding:0 16px; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; box-shadow:0 10px 24px rgba(15,28,51,.06); }}
    h1 {{ margin:0 0 10px; font-size:28px; }}
    h2 {{ margin:18px 0 8px; font-size:20px; }}
    .muted {{ color:#4f5d78; }}
    .row {{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:8px 0; }}
    .pill {{ border:1px solid var(--line); border-radius:999px; padding:6px 10px; font-size:12px; background:#f8faff; }}
    a, button {{ color:#fff; background:var(--accent); border:0; border-radius:8px; padding:10px 14px; text-decoration:none; cursor:pointer; font-weight:600; }}
    input {{ width:100%; padding:10px; border:1px solid var(--line); border-radius:8px; }}
    label {{ display:block; margin:10px 0 6px; font-weight:600; }}
    pre {{ white-space:pre-wrap; word-break:break-all; background:#0f172a; color:#d9e5ff; border-radius:8px; padding:12px; font-size:12px; }}
    .ok {{ color:var(--ok); font-weight:700; }}
    .err {{ color:var(--err); font-weight:700; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      {body}
    </div>
  </div>
</body>
</html>"""
    return page.encode("utf-8")


def app_ui_html() -> bytes:
    body = f"""
      <h1>{html.escape(SOLUTION.upper())} Runtime Screen</h1>
      <p class="muted">Execution status screen for the {html.escape(SOLUTION)} auth gateway.</p>
      <div class="row">
        <span class="pill">DB: {html.escape(DB_TYPE)}</span>
        <span class="pill">DB Name: {html.escape(DB_NAME)}</span>
        <span class="pill">Auth Port: {PORT}</span>
        <span class="pill">Password Policy: 123456</span>
      </div>
      <h2>Actions</h2>
      <div class="row">
        <a href="/login-ui">Open Login Screen</a>
        <a href="/members">View Member JSON</a>
        <a href="/health">Health</a>
      </div>
    """
    return render_html(f"{SOLUTION} runtime", body)


def login_ui_html() -> bytes:
    default_user = f"{SOLUTION}_member1"
    body = f"""
      <h1>{html.escape(SOLUTION.upper())} Login</h1>
      <p class="muted">Test login page for screenshot capture.</p>
      <label for="username">Username</label>
      <input id="username" value="{html.escape(default_user)}" />
      <label for="password">Password</label>
      <input id="password" type="password" value="123456" />
      <div class="row" style="margin-top:14px;">
        <button id="loginBtn">Login</button>
        <a href="/app-ui">Back</a>
      </div>
      <p id="status" class="muted"></p>
      <script>
        const statusEl = document.getElementById('status');
        document.getElementById('loginBtn').addEventListener('click', async () => {{
          const username = document.getElementById('username').value;
          const password = document.getElementById('password').value;
          statusEl.textContent = 'Logging in...';
          try {{
            const res = await fetch('/login', {{
              method: 'POST',
              headers: {{ 'Content-Type': 'application/json' }},
              body: JSON.stringify({{ username, password }})
            }});
            const data = await res.json();
            if (!res.ok) {{
              statusEl.className = 'err';
              statusEl.textContent = data.error || 'Login failed';
              return;
            }}
            statusEl.className = 'ok';
            statusEl.textContent = 'Login success';
            window.location.href = '/dashboard-ui?username=' + encodeURIComponent(data.username);
          }} catch (e) {{
            statusEl.className = 'err';
            statusEl.textContent = e.message;
          }}
        }});
      </script>
    """
    return render_html(f"{SOLUTION} login", body)


def dashboard_ui_html(username: str) -> bytes:
    safe_user = username if is_valid_username(username) else ""
    token = get_member_token(safe_user) if safe_user else ""
    body = f"""
      <h1>{html.escape(SOLUTION.upper())} Dashboard</h1>
      <p class="ok">Login completed.</p>
      <div class="row">
        <span class="pill">User: {html.escape(safe_user or 'unknown')}</span>
        <span class="pill">DB: {html.escape(DB_TYPE)}</span>
        <span class="pill">Token Updated: {'yes' if token else 'no'}</span>
      </div>
      <h2>JWT</h2>
      <pre>{html.escape(token or 'token not found')}</pre>
      <div class="row">
        <a href="/login-ui">Logout</a>
        <a href="/members">Member List JSON</a>
      </div>
    """
    return render_html(f"{SOLUTION} dashboard", body)


class Handler(BaseHTTPRequestHandler):
    server_version = "member-auth/3.0"

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def log_message(self, format: str, *args):
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            return self._json(
                200,
                {
                    "solution": SOLUTION,
                    "message": "Member auth API backed by solution RDBMS",
                    "db_type": DB_TYPE,
                    "db_name": DB_NAME,
                    "ui_endpoints": ["/app-ui", "/login-ui", "/dashboard-ui"],
                    "api_endpoints": ["/health", "/members", "/jwt/preissued", "/login"],
                },
            )

        if path == "/app-ui":
            return self._html(200, app_ui_html())

        if path == "/login-ui":
            return self._html(200, login_ui_html())

        if path == "/dashboard-ui":
            qs = parse_qs(parsed.query)
            username = qs.get("username", [""])[0]
            return self._html(200, dashboard_ui_html(username))

        if path == "/health":
            try:
                cnt = count_members()
            except Exception as exc:
                return self._json(
                    503,
                    {
                        "status": "error",
                        "solution": SOLUTION,
                        "error": str(exc),
                    },
                )
            return self._json(
                200,
                {
                    "status": "ok",
                    "solution": SOLUTION,
                    "members": cnt,
                    "port": PORT,
                    "db_type": DB_TYPE,
                },
            )

        if path == "/members":
            try:
                members = list_members()
            except Exception as exc:
                return self._json(503, {"error": str(exc)})
            return self._json(200, {"solution": SOLUTION, "members": members})

        if path == "/jwt/preissued":
            try:
                members = list_members()
            except Exception as exc:
                return self._json(503, {"error": str(exc)})
            tokens = [{"username": m["username"], "jwt_token": m["jwt_token"]} for m in members]
            return self._json(200, {"solution": SOLUTION, "tokens": tokens})

        return self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/login":
            return self._json(404, {"error": "not found"})

        try:
            payload = self._read_json()
        except json.JSONDecodeError:
            return self._json(400, {"error": "invalid json"})

        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", "")).strip()

        if not username or not password:
            return self._json(400, {"error": "username and password are required"})
        if not is_valid_username(username):
            return self._json(400, {"error": "invalid username format"})

        try:
            member = get_member(username)
        except Exception as exc:
            return self._json(503, {"error": str(exc)})

        if not member or member[1] != password:
            return self._json(401, {"error": "invalid credentials"})

        token = make_jwt(username)
        try:
            update_member_jwt(username, token)
        except Exception as exc:
            return self._json(503, {"error": str(exc)})

        return self._json(
            200,
            {
                "solution": SOLUTION,
                "username": username,
                "jwt_token": token,
                "token_type": "Bearer",
                "db_type": DB_TYPE,
                "password_policy": "all passwords are 123456 by policy",
            },
        )


def main() -> None:
    seed_members()
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[{SOLUTION}] member-auth listening on 0.0.0.0:{PORT} (db={DB_TYPE})", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
