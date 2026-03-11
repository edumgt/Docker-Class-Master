# Python 기반 5개 솔루션 통합 실행 레포

이 레포는 다음 5개 솔루션을 한 저장소에서 관리/실행하기 위한 통합 오케스트레이션 프로젝트입니다.

- Odoo
- ERPNext
- Zulip
- Taiga
- Tryton

요청사항 기준으로 다음을 구현했습니다.

- `solutions/` 하위 5개 폴더 구성
- `git clone/pull` 자동화 스크립트 제공 (`sync-solutions.sh`)
- Docker 기반 통합 실행 구성 (`docker-compose.yml`)
- 포트 충돌 없이 `9000~9100` 범위 사용
- 솔루션별 RDBMS 컨테이너 분리
- 모든 비밀번호 정책 `123456` 통일
- 솔루션별 회원 3명 + JWT 발급 API 제공
- 루트 `start.sh`, `stop.sh` 제공

## 1. 현재 환경에서의 Git 동기화 제약

현재 작업 환경에서는 GitHub DNS 해석이 차단되어 직접 clone/pull이 실패했습니다.
실제 확인된 에러:

- `fatal: unable to access 'https://github.com/...': Could not resolve host: github.com`

그래서 다음 방식으로 구성했습니다.

- `solutions/odoo`, `solutions/erpnext`, `solutions/zulip`, `solutions/taiga`, `solutions/tryton` 폴더를 먼저 생성
- `sync-solutions.sh`에서 네트워크 가능 시 `git clone --depth 1` 또는 `git pull --ff-only` 자동 수행
- 네트워크 대기 블로킹 방지를 위해 git 명령 타임아웃 기본값 `10초` 적용 (`GIT_TIMEOUT_SECONDS`로 조정 가능)
- 현재는 각 폴더를 로컬 git 저장소로 초기화하고 `origin` remote를 공식 URL로 연결
- 네트워크가 막힌 경우 폴더 유지 + remote 정보만 보존

네트워크가 열리면 아래만 실행하면 됩니다.

```bash
./sync-solutions.sh
```

## 2. 레포 구조

```text
.
├── docker-compose.yml
├── docker-compose.official-ui.yml
├── start.sh
├── stop.sh
├── start-official-ui.sh
├── stop-official-ui.sh
├── bootstrap-official-ui.sh
├── sync-solutions.sh
├── capture.sh
├── capture-official.sh
├── docker
│   ├── member-auth
│   │   ├── Dockerfile
│   │   └── server.py
│   └── db-init
│       ├── mariadb-erpnext.sql
│       ├── postgres-odoo.sql
│       ├── postgres-zulip.sql
│       ├── postgres-taiga.sql
│       └── postgres-tryton.sql
├── scripts
│   ├── capture-solution-ui.js
│   └── capture-official-ui.js
└── solutions
    ├── odoo
    ├── erpnext
    ├── zulip
    ├── taiga
    └── tryton
```

## 3. 포트 및 DB 매핑 (9000~9100 범위)

| 구분 | 서비스 | Host Port | Container Port | 비고 |
|---|---:|---:|---:|---|
| Odoo | `odoo-auth` | `9000` | `9000` | 로그인/JWT API |
| ERPNext | `erpnext-auth` | `9001` | `9000` | 로그인/JWT API |
| Zulip | `zulip-auth` | `9002` | `9000` | 로그인/JWT API |
| Taiga | `taiga-auth` | `9003` | `9000` | 로그인/JWT API |
| Tryton | `tryton-auth` | `9004` | `9000` | 로그인/JWT API |
| Odoo DB | `odoo-rdbms` | `9050` | `5432` | PostgreSQL |
| ERPNext DB | `erpnext-rdbms` | `9051` | `3306` | MariaDB |
| Zulip DB | `zulip-rdbms` | `9052` | `5432` | PostgreSQL |
| Taiga DB | `taiga-rdbms` | `9053` | `5432` | PostgreSQL |
| Tryton DB | `tryton-rdbms` | `9054` | `5432` | PostgreSQL |

모든 비밀번호는 정책상 `123456`으로 통일했습니다.

## 4. 회원/비밀번호/JWT 정책

각 솔루션별로 3개 계정을 자동 생성합니다.

- Odoo: `odoo_member1`, `odoo_member2`, `odoo_member3`
- ERPNext: `erpnext_member1`, `erpnext_member2`, `erpnext_member3`
- Zulip: `zulip_member1`, `zulip_member2`, `zulip_member3`
- Taiga: `taiga_member1`, `taiga_member2`, `taiga_member3`
- Tryton: `tryton_member1`, `tryton_member2`, `tryton_member3`

공통 비밀번호:

- `123456`

저장 위치:

- 각 솔루션의 RDBMS 컨테이너 내부 `members` 테이블
- auth API는 해당 RDBMS를 직접 조회하여 로그인 검증 및 JWT 갱신 수행

JWT 정책:

- 서명 알고리즘: HS256
- 시크릿: `123456`
- 로그인 시 신규 JWT 재발급
- `/jwt/preissued`에서 사전 발급 토큰 조회 가능

## 5. 실행 방법

### 5.1 전체 시작

```bash
./start.sh
```

`start.sh`에서 수행하는 작업:

1. `./sync-solutions.sh` 실행 (clone/pull 시도)
2. BuildKit 비활성화 환경변수 자동 적용 (`DOCKER_BUILDKIT=0`, `COMPOSE_DOCKER_CLI_BUILD=0`)
3. `docker compose up -d --build`
4. 서비스 상태 출력

### 5.2 전체 중지

```bash
./stop.sh
```

볼륨까지 삭제하려면:

```bash
./stop.sh --volumes
```

### 5.3 공식 제품 UI 스택 시작/중지

공식 제품 웹앱(9060~9064)과 해당 RDBMS/보조 컴포넌트를 실행하려면:

```bash
./start-official-ui.sh
```

`start-official-ui.sh`는 아래를 자동 수행합니다.

1. `docker-compose.official-ui.yml` 기반 컨테이너 기동
2. `bootstrap-official-ui.sh` 실행
3. Odoo/ERPNext/Tryton/Zulip 초기 설정 및 관리자 계정 정렬

중지:

```bash
./stop-official-ui.sh
```

볼륨까지 삭제:

```bash
./stop-official-ui.sh --volumes
```

## 6. API 사용 예시 (로그인/JWT)

### 6.1 Odoo 계정 로그인

```bash
curl -s -X POST http://localhost:9000/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"odoo_member1","password":"123456"}'
```

### 6.2 ERPNext 계정 로그인

```bash
curl -s -X POST http://localhost:9001/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"erpnext_member1","password":"123456"}'
```

### 6.3 솔루션별 회원 목록 확인

```bash
curl -s http://localhost:9002/members
curl -s http://localhost:9003/members
curl -s http://localhost:9004/members
```

### 6.4 헬스체크

```bash
curl -s http://localhost:9000/health
curl -s http://localhost:9001/health
curl -s http://localhost:9002/health
curl -s http://localhost:9003/health
curl -s http://localhost:9004/health
```

## 7. 솔루션별 분석 및 실제 운용 시 실행 포인트

아래는 각 솔루션을 실제 원본 코드 기준으로 운용할 때의 핵심 포인트입니다.

### 7.1 Odoo

- 분류: ERP + 업무 통합 플랫폼
- 핵심 DB: PostgreSQL
- 운영 포인트:
  - 모듈 단위 확장성 높음
  - 초기 설정 후 사용자/권한 체계 정교화 필요

### 7.2 ERPNext

- 분류: ERP + Desk 기반 업무 포털
- 핵심 DB: MariaDB
- 운영 포인트:
  - Frappe/Bench 기반 구성 이해 필요
  - Redis/worker 등 주변 컴포넌트까지 포함한 운영 설계 권장

### 7.3 Zulip

- 분류: 협업 메신저
- 핵심 DB: PostgreSQL
- 운영 포인트:
  - 실사용 시 메일/알림/파일스토리지 구성 필요
  - 조직 온보딩/채널 정책 설계 중요

### 7.4 Taiga

- 분류: 프로젝트 관리(칸반/스프린트)
- 핵심 DB: PostgreSQL
- 운영 포인트:
  - 백로그/스프린트 워크플로우 표준화 효과 큼
  - 사용자 관리/권한을 조직 프로세스와 맞춰야 함

### 7.5 Tryton

- 분류: 모듈형 비즈니스 소프트웨어
- 핵심 DB: PostgreSQL
- 운영 포인트:
  - 모듈 조합 및 도메인 모델 설계 역량이 중요
  - 대형 패키지보다 컴포넌트 지향 도입에 적합

## 8. 중요 참고

- 본 레포는 5개 솔루션을 한 번에 관리하기 위한 통합 실행 템플릿입니다.
- 실제 원본 코드를 이 레포에 완전한 형태로 포함하려면, 네트워크가 허용된 환경에서 `./sync-solutions.sh`를 먼저 성공시켜야 합니다.
- 현재 구성에서는 “요청된 비밀번호 통일, 회원 3명, JWT 발급, Docker 일괄 실행/중지”를 우선 충족하도록 설계했습니다.

## 9. 실제 검증 결과

검증 일시: 2026-03-01

- `docker compose up -d --build`: 성공
- DB 컨테이너 5개 + auth 컨테이너 5개 모두 `healthy` 확인
- `members` 테이블 건수: 각 DB 모두 3건 확인
- 5개 auth API 모두 `/health`, `/login` 성공 및 JWT 발급 확인
- 로그인 후 DB의 `members.jwt_token` 갱신 확인 (RDBMS 직접 연동 검증)

참고:

- 현재 실행 환경은 호스트 `localhost` 포트 접근이 격리되어 있어, 검증은 `docker compose exec` 기반 내부 호출로 수행했습니다.
- 일반 Docker 환경에서는 README의 `curl http://localhost:9000~9004` 방식으로 직접 호출 가능합니다.

## 10. 빠른 명령 모음

```bash
# 시작
./start.sh

# 상태
docker compose ps

# 중지
./stop.sh

# 중지 + 데이터 삭제
./stop.sh --volumes

# 소스 동기화 재시도
./sync-solutions.sh

# 공식 제품 UI 시작/중지
./start-official-ui.sh
./stop-official-ui.sh

# 공식 제품 UI 중지 + 데이터 삭제
./stop-official-ui.sh --volumes
```

## 11. 화면 캡처 (실행/로그인/대시보드)

각 솔루션별로 다음 3가지 화면을 자동 캡처할 수 있습니다.

- 실행 화면: `/app-ui`
- 로그인 화면: `/login-ui`
- 로그인 후 대시보드: `/dashboard-ui?username=<solution>_member1`

실행:

```bash
./capture.sh
```

생성 경로:

- `captures/odoo/01-runtime.png`
- `captures/odoo/02-login.png`
- `captures/odoo/03-dashboard.png`
- `captures/erpnext/01-runtime.png`
- `captures/erpnext/02-login.png`
- `captures/erpnext/03-dashboard.png`
- `captures/zulip/01-runtime.png`
- `captures/zulip/02-login.png`
- `captures/zulip/03-dashboard.png`
- `captures/taiga/01-runtime.png`
- `captures/taiga/02-login.png`
- `captures/taiga/03-dashboard.png`
- `captures/tryton/01-runtime.png`
- `captures/tryton/02-login.png`
- `captures/tryton/03-dashboard.png`
- `captures/summary.json`

참고:

- 캡처는 현재 레포에서 구성한 auth gateway UI 기준입니다.
- 각 원본 제품(Odoo/ERPNext/Zulip/Taiga/Tryton) 공식 웹앱의 실제 대시보드 캡처는 아래 12번 절차로 수행합니다.

## 12. 공식 제품 UI 캡처 (실행/로그인/대시보드)

공식 제품 포트(모두 `9000~9100` 범위):

- Odoo: `9060`
- ERPNext: `9061` (`official.local` Host 기반)
- Tryton: `9062`
- Taiga Front: `9063`
- Zulip: `9064`

참고:

- Zulip 공식 UI 로그인 캡처를 위해 `zulip-official-rabbitmq`, `zulip-official-redis` 보조 컨테이너를 함께 사용합니다.

실행:

```bash
./start-official-ui.sh
./capture-official.sh
```

브라우저에서 ERPNext를 직접 확인할 때는 Host 헤더가 필요하므로 로컬 hosts 설정에 아래를 추가하세요.

```text
127.0.0.1 official.local
```

생성 경로:

- `captures_official/odoo/01-runtime.png`
- `captures_official/odoo/02-login.png`
- `captures_official/odoo/03-dashboard.png`
- `captures_official/erpnext/01-runtime.png`
- `captures_official/erpnext/02-login.png`
- `captures_official/erpnext/03-dashboard.png`
- `captures_official/tryton/01-runtime.png`
- `captures_official/tryton/02-login.png`
- `captures_official/tryton/03-dashboard.png`
- `captures_official/taiga/01-runtime.png`
- `captures_official/taiga/02-login.png`
- `captures_official/taiga/03-dashboard.png`
- `captures_official/zulip/01-runtime.png`
- `captures_official/zulip/02-login.png`
- `captures_official/zulip/03-dashboard.png`
- `captures_official/summary.json`

`summary.json`에는 솔루션별 캡처 성공 상태가 기록됩니다.

최신 검증 시각: `2026-03-01 14:17:08 KST` (`captures_official/summary.json`)

2026-03-01 기준 검증 결과:

- Odoo: `ok`
- ERPNext: `ok`
- Tryton: `ok`
- Taiga: `ok`
- Zulip: `ok`
