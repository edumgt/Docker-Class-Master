#!/usr/bin/env python3
# 이 서버는 온프레미스 솔루션(Odoo, ERPNext 등)의 멤버 인증 게이트웨이입니다.
# JWT 발급, 로그인 API, 회원 관리 UI를 단일 Python HTTP 서버로 제공합니다.

import base64     # JWT 헤더/페이로드를 Base64URL 인코딩하기 위한 표준 라이브러리
import hashlib    # HMAC-SHA256 서명 생성에 사용되는 해시 알고리즘 라이브러리
import hmac       # 안전한 메시지 인증 코드(HMAC) 생성용 라이브러리
import html       # HTML 특수 문자 이스케이프 처리 (XSS 방지)
import json       # JSON 직렬화/역직렬화 라이브러리
import os         # 환경 변수 읽기 및 프로세스 환경 복사용 표준 라이브러리
import re         # 사용자명 유효성 검사를 위한 정규표현식 라이브러리
import subprocess # DB 클라이언트(psql, mariadb) 명령어 실행용 라이브러리
import time       # JWT 발급/만료 시각 계산용 시간 라이브러리
from http.server import BaseHTTPRequestHandler, HTTPServer  # 기본 HTTP 서버 구현
from urllib.parse import parse_qs, urlparse  # URL 경로 및 쿼리 파라미터 파싱

# ─── 환경 변수에서 서버 설정값 읽기 (기본값은 실습용 개발 환경 값) ───
SOLUTION = os.getenv("SOLUTION", "solution")       # 솔루션 이름 (DB명, 사용자명 접두사에 사용)
PORT = int(os.getenv("PORT", "9000"))              # HTTP 서버 수신 포트
JWT_SECRET = os.getenv("JWT_SECRET", "123456")    # JWT 서명 비밀키 (운영 환경에서는 반드시 변경)
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "123456")  # 시드 멤버의 기본 비밀번호
TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "2592000"))
# 토큰 유효 기간(초): 기본값 30일 (2592000 = 30 × 24 × 60 × 60)

# ─── DB 접속 설정 (환경 변수로 오버라이드 가능) ───
DB_TYPE = os.getenv("DB_TYPE", "postgres")  # DB 종류: "postgres" 또는 "mariadb"
DB_HOST = os.getenv("DB_HOST", "localhost") # DB 서버 호스트명
DB_PORT = os.getenv("DB_PORT", "5432")      # DB 포트 (문자열로 유지 - subprocess 명령어 인자로 사용)
DB_NAME = os.getenv("DB_NAME", SOLUTION)    # 접속할 DB 이름 (기본값: 솔루션 이름)
DB_USER = os.getenv("DB_USER", SOLUTION)    # DB 사용자명 (기본값: 솔루션 이름)
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")  # DB 비밀번호

# 초기 삽입할 시드(seed) 멤버 목록 생성
SEED_USERS = [
    f"{SOLUTION}_member1",  # 첫 번째 테스트 멤버 (예: solution_member1)
    f"{SOLUTION}_member2",  # 두 번째 테스트 멤버
    f"{SOLUTION}_member3",  # 세 번째 테스트 멤버
]

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,64}$")
# 유효한 사용자명 패턴: 영문자, 숫자, 언더스코어만 허용, 길이 3~64자


def b64url(data: bytes) -> str:
    """바이트 데이터를 Base64URL(패딩 없음) 형식으로 인코딩하여 문자열로 반환합니다."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")
    # urlsafe_b64encode: URL 안전 문자(+→-, /→_)를 사용하는 Base64 인코딩
    # .rstrip(b"="): JWT 표준에 따라 패딩 문자("=") 제거
    # .decode("ascii"): bytes → str 변환


def make_jwt(username: str) -> str:
    """주어진 사용자명으로 HS256 서명 JWT 토큰을 생성하여 반환합니다."""
    now = int(time.time())  # 현재 Unix 타임스탬프 (발급 시각)
    header = {"alg": "HS256", "typ": "JWT"}  # JWT 헤더: 알고리즘과 타입 지정
    payload = {
        "sub": username,                    # subject: 토큰 주체 (사용자명)
        "solution": SOLUTION,               # 커스텀 클레임: 솔루션 이름
        "iat": now,                         # issued at: 발급 시각
        "exp": now + TOKEN_TTL_SECONDS,     # expiration: 만료 시각 (현재 + TTL)
    }
    header_part = b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    # 헤더를 최소화된 JSON 문자열로 직렬화 후 Base64URL 인코딩
    payload_part = b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    # 페이로드를 최소화된 JSON 문자열로 직렬화 후 Base64URL 인코딩
    signing_input = f"{header_part}.{payload_part}"
    # JWT 서명 대상: "헤더.페이로드" 형식의 문자열
    signature = hmac.new(
        JWT_SECRET.encode("utf-8"),          # 서명 비밀키 (bytes로 변환)
        signing_input.encode("utf-8"),       # 서명할 데이터 (bytes로 변환)
        hashlib.sha256                        # 사용할 해시 알고리즘: SHA-256
    ).digest()  # 바이너리 서명 생성
    return f"{signing_input}.{b64url(signature)}"
    # 최종 JWT: "헤더.페이로드.서명" 형식


def is_valid_username(username: str) -> bool:
    """사용자명이 허용된 패턴(영문/숫자/언더스코어, 3~64자)에 맞는지 검증합니다."""
    return bool(USERNAME_PATTERN.fullmatch(username))
    # fullmatch: 전체 문자열이 패턴과 일치할 때만 True (부분 일치 제외)


def run_sql(sql: str) -> str:
    """DB 종류에 맞는 CLI 클라이언트를 subprocess로 실행하여 SQL을 수행하고 출력을 반환합니다."""
    if DB_TYPE == "postgres":
        env = os.environ.copy()        # 현재 프로세스 환경 변수 복사
        env["PGPASSWORD"] = DB_PASSWORD  # psql 비밀번호를 환경 변수로 설정 (보안: 명령줄에 노출 방지)
        cmd = [
            "psql",                    # PostgreSQL CLI 클라이언트
            "-h", DB_HOST,             # 호스트 지정
            "-p", DB_PORT,             # 포트 지정
            "-U", DB_USER,             # 사용자명 지정
            "-d", DB_NAME,             # DB 이름 지정
            "-At",                     # -A: 정렬 없는 출력, -t: 헤더/요약 없이 데이터만 출력
            "-F", "\t",                # 컬럼 구분자를 탭으로 설정
            "-c", sql,                 # 실행할 SQL 문
        ]
    elif DB_TYPE == "mariadb":
        cmd = [
            "mariadb",                 # MariaDB CLI 클라이언트
            "-h", DB_HOST,             # 호스트 지정
            "-P", DB_PORT,             # 포트 지정 (대문자 P)
            "-u", DB_USER,             # 사용자명 지정
            f"-p{DB_PASSWORD}",        # 비밀번호 (-p에 붙여서 지정, 공백 없음)
            f"-D{DB_NAME}",            # DB 이름 (-D에 붙여서 지정)
            "-N",                      # 컬럼 헤더 제외
            "-B",                      # 배치 모드 (탭 구분자)
            "-e", sql,                 # 실행할 SQL 문
        ]
        env = None  # MariaDB는 환경 변수 대신 명령줄 인자로 비밀번호 전달
    else:
        raise RuntimeError(f"Unsupported DB_TYPE: {DB_TYPE}")
        # 지원하지 않는 DB 종류는 RuntimeError 발생

    cp = subprocess.run(
        cmd,
        env=env,              # 설정된 환경 변수 전달
        check=True,           # 명령 실패(비 0 종료 코드) 시 CalledProcessError 발생
        capture_output=True,  # stdout/stderr를 캡처하여 cp.stdout, cp.stderr에 저장
        text=True,            # 출력을 bytes 대신 str로 반환
    )
    return cp.stdout.strip()  # 표준 출력의 앞뒤 공백/개행 제거 후 반환


def sql_esc(value: str) -> str:
    """SQL 문자열 값 내의 작은따옴표(')를 두 개('')로 이스케이프하여 SQL 인젝션을 방지합니다."""
    return value.replace("'", "''")
    # SQL 표준 이스케이프: 작은따옴표를 두 개 연속으로 치환


def seed_members() -> None:
    """초기 시드 멤버 목록을 DB에 삽입하거나 기존 레코드를 업데이트합니다."""
    if DB_TYPE == "postgres":
        for username in SEED_USERS:
            token = make_jwt(username)  # 각 멤버에 대한 JWT 토큰 생성
            sql = (
                "INSERT INTO members (username, password, jwt_token) "
                f"VALUES ('{sql_esc(username)}', '{sql_esc(DEFAULT_PASSWORD)}', '{sql_esc(token)}') "
                "ON CONFLICT (username) DO UPDATE SET "
                "password = EXCLUDED.password, jwt_token = EXCLUDED.jwt_token;"
                # PostgreSQL UPSERT: 사용자명 충돌 시 비밀번호와 토큰만 업데이트
            )
            run_sql(sql)  # SQL 실행
    elif DB_TYPE == "mariadb":
        for username in SEED_USERS:
            token = make_jwt(username)  # 각 멤버에 대한 JWT 토큰 생성
            sql = (
                "INSERT INTO members (username, password, jwt_token) "
                f"VALUES ('{sql_esc(username)}', '{sql_esc(DEFAULT_PASSWORD)}', '{sql_esc(token)}') "
                "ON DUPLICATE KEY UPDATE "
                "password = VALUES(password), jwt_token = VALUES(jwt_token);"
                # MariaDB UPSERT: 중복 키(사용자명) 시 비밀번호와 토큰만 업데이트
            )
            run_sql(sql)  # SQL 실행


def count_members() -> int:
    """members 테이블의 전체 행 수를 반환합니다."""
    out = run_sql("SELECT COUNT(*) FROM members;")  # 멤버 수를 SQL로 조회
    return int(out.splitlines()[-1]) if out else 0
    # 출력의 마지막 줄을 정수로 변환 (출력이 없으면 0 반환)


def list_members() -> list[dict]:
    """members 테이블의 모든 멤버를 사용자명 순으로 조회하여 딕셔너리 목록으로 반환합니다."""
    out = run_sql("SELECT username, password, jwt_token FROM members ORDER BY username;")
    if not out:
        return []  # 결과가 없으면 빈 리스트 반환
    rows = []
    for line in out.splitlines():
        # 각 줄을 탭으로 분리하여 컬럼 파싱
        parts = line.split("\t")
        if len(parts) < 3:
            continue  # 컬럼이 3개 미만인 줄은 건너뜀 (데이터 이상 방지)
        rows.append(
            {
                "username": parts[0],    # 첫 번째 컬럼: 사용자명
                "password": parts[1],    # 두 번째 컬럼: 비밀번호
                "jwt_token": parts[2],   # 세 번째 컬럼: JWT 토큰
            }
        )
    return rows  # 파싱된 멤버 목록 반환


def get_member(username: str) -> tuple[str, str] | None:
    """특정 사용자명으로 멤버의 (사용자명, 비밀번호) 튜플을 조회합니다. 없으면 None을 반환합니다."""
    safe = sql_esc(username)  # SQL 인젝션 방지용 이스케이프 처리
    out = run_sql(f"SELECT username, password FROM members WHERE username = '{safe}' LIMIT 1;")
    if not out:
        return None  # 결과가 없으면 None 반환
    line = out.splitlines()[0]   # 첫 번째 결과 줄 선택
    parts = line.split("\t")     # 탭으로 컬럼 분리
    if len(parts) < 2:
        return None  # 컬럼이 2개 미만이면 유효하지 않은 결과로 판단
    return parts[0], parts[1]    # (사용자명, 비밀번호) 튜플 반환


def get_member_token(username: str) -> str:
    """특정 사용자명의 저장된 JWT 토큰을 반환합니다. 없으면 빈 문자열을 반환합니다."""
    safe = sql_esc(username)  # SQL 인젝션 방지용 이스케이프 처리
    out = run_sql(f"SELECT jwt_token FROM members WHERE username = '{safe}' LIMIT 1;")
    if not out:
        return ""  # 결과가 없으면 빈 문자열 반환
    return out.splitlines()[0]  # 첫 번째 줄(JWT 토큰) 반환


def update_member_jwt(username: str, token: str) -> None:
    """특정 멤버의 JWT 토큰을 새 토큰으로 업데이트합니다."""
    safe_user = sql_esc(username)  # 사용자명 SQL 이스케이프
    safe_tok = sql_esc(token)      # 토큰 SQL 이스케이프
    run_sql(f"UPDATE members SET jwt_token = '{safe_tok}' WHERE username = '{safe_user}';")
    # 해당 사용자의 jwt_token 컬럼을 새 토큰으로 업데이트


def render_html(title: str, body: str) -> bytes:
    """공통 HTML 레이아웃에 title과 body를 삽입하여 완성된 HTML 페이지를 bytes로 반환합니다."""
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <!-- html.escape(title): 제목의 HTML 특수문자 이스케이프 처리 (XSS 방지) -->
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
    return page.encode("utf-8")  # HTML 문자열을 UTF-8 바이트로 인코딩하여 반환


def app_ui_html() -> bytes:
    """런타임 상태 화면 HTML을 생성하여 반환합니다 (솔루션 정보 및 주요 링크 표시)."""
    body = f"""
      <h1>{html.escape(SOLUTION.upper())} Runtime Screen</h1>
      <!-- html.escape: 솔루션 이름의 HTML 특수문자 이스케이프 -->
      <p class="muted">Execution status screen for the {html.escape(SOLUTION)} auth gateway.</p>
      <div class="row">
        <span class="pill">DB: {html.escape(DB_TYPE)}</span>      <!-- DB 종류 표시 -->
        <span class="pill">DB Name: {html.escape(DB_NAME)}</span>  <!-- DB 이름 표시 -->
        <span class="pill">Auth Port: {PORT}</span>                 <!-- 인증 서버 포트 표시 -->
        <span class="pill">Password Policy: 123456</span>           <!-- 비밀번호 정책 안내 -->
      </div>
      <h2>Actions</h2>
      <div class="row">
        <a href="/login-ui">Open Login Screen</a>   <!-- 로그인 화면으로 이동 -->
        <a href="/members">View Member JSON</a>     <!-- 멤버 목록 JSON 조회 -->
        <a href="/health">Health</a>                <!-- 헬스체크 API 링크 -->
      </div>
    """
    return render_html(f"{SOLUTION} runtime", body)  # 공통 레이아웃으로 HTML 완성


def login_ui_html() -> bytes:
    """로그인 테스트 화면 HTML을 생성하여 반환합니다 (브라우저 스크린샷 캡처용)."""
    default_user = f"{SOLUTION}_member1"  # 기본 입력값으로 첫 번째 시드 멤버 사용
    body = f"""
      <h1>{html.escape(SOLUTION.upper())} Login</h1>
      <p class="muted">Test login page for screenshot capture.</p>
      <label for="username">Username</label>
      <input id="username" value="{html.escape(default_user)}" />  <!-- 기본값 사용자명 -->
      <label for="password">Password</label>
      <input id="password" type="password" value="123456" />  <!-- 기본값 비밀번호 -->
      <div class="row" style="margin-top:14px;">
        <button id="loginBtn">Login</button>  <!-- 로그인 버튼 -->
        <a href="/app-ui">Back</a>            <!-- 이전 화면으로 돌아가기 -->
      </div>
      <p id="status" class="muted"></p>  <!-- 로그인 결과 메시지 출력 영역 -->
      <script>
        const statusEl = document.getElementById('status');  // 상태 표시 요소 참조
        document.getElementById('loginBtn').addEventListener('click', async () => {{
          const username = document.getElementById('username').value;  // 입력된 사용자명
          const password = document.getElementById('password').value;  // 입력된 비밀번호
          statusEl.textContent = 'Logging in...';  // 로그인 시도 중 메시지
          try {{
            const res = await fetch('/login', {{
              method: 'POST',
              headers: {{ 'Content-Type': 'application/json' }},
              body: JSON.stringify({{ username, password }})  // JSON 형식으로 자격증명 전송
            }});
            const data = await res.json();  // 응답 JSON 파싱
            if (!res.ok) {{
              statusEl.className = 'err';                          // 오류 스타일 적용
              statusEl.textContent = data.error || 'Login failed'; // 오류 메시지 표시
              return;
            }}
            statusEl.className = 'ok';                 // 성공 스타일 적용
            statusEl.textContent = 'Login success';   // 성공 메시지 표시
            window.location.href = '/dashboard-ui?username=' + encodeURIComponent(data.username);
            // 로그인 성공 시 대시보드로 리다이렉트 (사용자명을 쿼리 파라미터로 전달)
          }} catch (e) {{
            statusEl.className = 'err';
            statusEl.textContent = e.message;  // 네트워크 오류 등 예외 메시지 표시
          }}
        }});
      </script>
    """
    return render_html(f"{SOLUTION} login", body)  # 공통 레이아웃으로 HTML 완성


def dashboard_ui_html(username: str) -> bytes:
    """로그인 완료 후 대시보드 화면 HTML을 생성하여 반환합니다 (JWT 토큰 표시 포함)."""
    safe_user = username if is_valid_username(username) else ""
    # 사용자명 유효성 검증: 유효하지 않으면 빈 문자열로 처리 (안전한 기본값)
    token = get_member_token(safe_user) if safe_user else ""
    # 유효한 사용자명이 있을 때만 DB에서 JWT 토큰 조회
    body = f"""
      <h1>{html.escape(SOLUTION.upper())} Dashboard</h1>
      <p class="ok">Login completed.</p>  <!-- 로그인 완료 메시지 -->
      <div class="row">
        <span class="pill">User: {html.escape(safe_user or 'unknown')}</span>
        <!-- 사용자명 표시 (유효하지 않으면 'unknown' 표시) -->
        <span class="pill">DB: {html.escape(DB_TYPE)}</span>  <!-- DB 종류 표시 -->
        <span class="pill">Token Updated: {'yes' if token else 'no'}</span>
        <!-- JWT 토큰 존재 여부 표시 -->
      </div>
      <h2>JWT</h2>
      <pre>{html.escape(token or 'token not found')}</pre>
      <!-- JWT 토큰 내용 표시 (없으면 'token not found', html.escape로 XSS 방지) -->
      <div class="row">
        <a href="/login-ui">Logout</a>          <!-- 로그인 화면으로 돌아가기 -->
        <a href="/members">Member List JSON</a>  <!-- 전체 멤버 목록 JSON 조회 -->
      </div>
    """
    return render_html(f"{SOLUTION} dashboard", body)  # 공통 레이아웃으로 HTML 완성


class Handler(BaseHTTPRequestHandler):
    """모든 HTTP 요청을 처리하는 핸들러 클래스 (GET/POST 라우팅 포함)."""

    server_version = "member-auth/3.0"  # Server 응답 헤더에 표시되는 서버 버전 문자열

    def _json(self, status: int, payload: dict) -> None:
        """JSON 응답을 구성하여 클라이언트에 전송하는 헬퍼 메서드."""
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        # ensure_ascii=False: 비ASCII 문자(한글 등)를 유니코드 이스케이프 없이 그대로 출력
        self.send_response(status)                                       # HTTP 상태 코드 전송
        self.send_header("Content-Type", "application/json; charset=utf-8")  # JSON MIME 타입 헤더
        self.send_header("Content-Length", str(len(body)))               # 응답 본문 바이트 크기
        self.end_headers()                                               # 헤더 전송 완료
        self.wfile.write(body)                                           # 응답 본문(JSON) 전송

    def _html(self, status: int, body: bytes) -> None:
        """HTML 응답을 구성하여 클라이언트에 전송하는 헬퍼 메서드."""
        self.send_response(status)                                       # HTTP 상태 코드 전송
        self.send_header("Content-Type", "text/html; charset=utf-8")    # HTML MIME 타입 헤더
        self.send_header("Content-Length", str(len(body)))               # 응답 본문 바이트 크기
        self.end_headers()                                               # 헤더 전송 완료
        self.wfile.write(body)                                           # 응답 본문(HTML) 전송

    def _read_json(self) -> dict:
        """요청 본문을 읽어 JSON으로 파싱하여 딕셔너리로 반환합니다. 본문이 없으면 빈 딕셔너리를 반환합니다."""
        length = int(self.headers.get("Content-Length", "0"))  # Content-Length 헤더에서 본문 크기 읽기
        if length <= 0:
            return {}  # 본문이 없으면 빈 딕셔너리 반환
        raw = self.rfile.read(length)  # 지정된 바이트 수만큼 요청 본문 읽기
        if not raw:
            return {}  # 실제 데이터가 없으면 빈 딕셔너리 반환
        return json.loads(raw.decode("utf-8"))  # UTF-8 디코딩 후 JSON 파싱

    def log_message(self, format: str, *args):
        """기본 HTTP 서버의 콘솔 접근 로그 출력을 억제합니다."""
        return  # 아무것도 출력하지 않음 (로그 노이즈 방지)

    def do_GET(self) -> None:
        """HTTP GET 요청을 경로별로 라우팅하여 처리합니다."""
        parsed = urlparse(self.path)   # 요청 경로를 파싱하여 path, query 분리
        path = parsed.path             # 경로 부분만 추출 (쿼리스트링 제외)

        if path == "/":
            # 루트 경로: API 서버 정보를 JSON으로 반환
            return self._json(
                200,
                {
                    "solution": SOLUTION,                        # 솔루션 이름
                    "message": "Member auth API backed by solution RDBMS",  # 서버 설명
                    "db_type": DB_TYPE,                          # 사용 중인 DB 종류
                    "db_name": DB_NAME,                          # 사용 중인 DB 이름
                    "ui_endpoints": ["/app-ui", "/login-ui", "/dashboard-ui"],    # UI 엔드포인트 목록
                    "api_endpoints": ["/health", "/members", "/jwt/preissued", "/login"],  # API 엔드포인트 목록
                },
            )

        if path == "/app-ui":
            # 런타임 상태 화면 HTML 반환
            return self._html(200, app_ui_html())

        if path == "/login-ui":
            # 로그인 UI 화면 HTML 반환
            return self._html(200, login_ui_html())

        if path == "/dashboard-ui":
            # 대시보드 화면: URL 쿼리에서 username 파라미터 추출
            qs = parse_qs(parsed.query)             # 쿼리스트링 파싱 (예: ?username=alice)
            username = qs.get("username", [""])[0]  # username 파라미터 값 추출 (없으면 빈 문자열)
            return self._html(200, dashboard_ui_html(username))

        if path == "/health":
            # 헬스체크: DB 연결 및 멤버 수를 확인하여 서비스 상태 반환
            try:
                cnt = count_members()  # DB에서 멤버 수 조회 (DB 연결 상태도 확인)
            except Exception as exc:
                return self._json(
                    503,  # 503 Service Unavailable: DB 오류
                    {
                        "status": "error",
                        "solution": SOLUTION,
                        "error": str(exc),  # 오류 메시지 포함
                    },
                )
            return self._json(
                200,
                {
                    "status": "ok",         # 정상 상태
                    "solution": SOLUTION,   # 솔루션 이름
                    "members": cnt,         # 현재 멤버 수
                    "port": PORT,           # 서비스 포트
                    "db_type": DB_TYPE,     # DB 종류
                },
            )

        if path == "/members":
            # 전체 멤버 목록을 JSON으로 반환
            try:
                members = list_members()  # DB에서 모든 멤버 조회
            except Exception as exc:
                return self._json(503, {"error": str(exc)})  # DB 오류 시 503 반환
            return self._json(200, {"solution": SOLUTION, "members": members})

        if path == "/jwt/preissued":
            # 모든 멤버의 사전 발급 JWT 토큰 목록을 반환 (실습 편의용)
            try:
                members = list_members()  # 전체 멤버 조회
            except Exception as exc:
                return self._json(503, {"error": str(exc)})  # DB 오류 시 503 반환
            tokens = [{"username": m["username"], "jwt_token": m["jwt_token"]} for m in members]
            # 각 멤버의 사용자명과 JWT 토큰만 추출
            return self._json(200, {"solution": SOLUTION, "tokens": tokens})

        return self._json(404, {"error": "not found"})  # 정의되지 않은 경로는 404 반환

    def do_POST(self) -> None:
        """HTTP POST 요청을 처리합니다. /login 경로에서만 로그인 처리를 수행합니다."""
        path = urlparse(self.path).path  # 요청 경로 파싱
        if path != "/login":
            return self._json(404, {"error": "not found"})  # /login 외 경로는 404 반환

        try:
            payload = self._read_json()  # 요청 본문을 JSON으로 파싱
        except json.JSONDecodeError:
            return self._json(400, {"error": "invalid json"})  # JSON 파싱 실패 시 400 반환

        username = str(payload.get("username", "")).strip()  # 사용자명 추출 및 앞뒤 공백 제거
        password = str(payload.get("password", "")).strip()  # 비밀번호 추출 및 앞뒤 공백 제거

        if not username or not password:
            return self._json(400, {"error": "username and password are required"})
            # 사용자명 또는 비밀번호가 비어있으면 400 에러 반환

        if not is_valid_username(username):
            return self._json(400, {"error": "invalid username format"})
            # 사용자명 형식이 유효하지 않으면 400 에러 반환

        try:
            member = get_member(username)  # DB에서 해당 사용자명의 멤버 조회
        except Exception as exc:
            return self._json(503, {"error": str(exc)})  # DB 오류 시 503 반환

        if not member or member[1] != password:
            return self._json(401, {"error": "invalid credentials"})
            # 멤버가 없거나 비밀번호 불일치 시 401 Unauthorized 반환

        token = make_jwt(username)  # 인증 성공 시 새 JWT 토큰 발급

        try:
            update_member_jwt(username, token)  # 발급된 토큰을 DB에 저장
        except Exception as exc:
            return self._json(503, {"error": str(exc)})  # DB 저장 실패 시 503 반환

        return self._json(
            200,
            {
                "solution": SOLUTION,           # 솔루션 이름
                "username": username,            # 인증된 사용자명
                "jwt_token": token,              # 발급된 JWT 토큰
                "token_type": "Bearer",          # 토큰 타입 (HTTP Authorization 헤더 형식)
                "db_type": DB_TYPE,              # 사용 중인 DB 종류
                "password_policy": "all passwords are 123456 by policy",  # 비밀번호 정책 안내
            },
        )


def main() -> None:
    """서버 진입점: 시드 멤버 삽입 후 HTTP 서버를 시작합니다."""
    seed_members()  # 초기 테스트 멤버 데이터를 DB에 삽입 (없으면 생성, 있으면 업데이트)
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    # HTTPServer: 모든 네트워크 인터페이스(0.0.0.0)에서 PORT로 수신하는 단일 스레드 서버 생성
    print(f"[{SOLUTION}] member-auth listening on 0.0.0.0:{PORT} (db={DB_TYPE})", flush=True)
    # flush=True: 출력 버퍼를 즉시 비워 컨테이너 로그에서 즉시 확인 가능
    server.serve_forever()  # 서버를 무한 루프로 실행 (Ctrl+C로 종료)


if __name__ == "__main__":
    main()  # 이 파일이 직접 실행될 때만 main() 호출 (모듈로 임포트 시 실행하지 않음)
