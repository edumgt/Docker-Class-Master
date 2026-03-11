# 전체 커리큘럼 (총 70시간)

> **10일 × 7시간** (권장: 강의 30~40% / 실습 60~70%)

## Day 1 — Docker 개요 & 컨테이너 첫 걸음 (7H)
**목표:** “왜 Docker인가” + 이미지/컨테이너/레지스트리 기본 흐름 이해

- 가상화 vs 컨테이너, OCI 개요
- 설치/환경 점검 (Docker Desktop/Engine, WSL2 이슈)
- 기본 CLI: `run/ps/stop/rm/logs/exec/cp`
- 컨테이너 생명주기, restart policy
- 미니랩: nginx 컨테이너 + 포트 바인딩 + 로그 확인

➡️ 실습: `labs/day01/README.md`

---

## Day 2 — 컨테이너 다루기 심화(프로세스/자원/IO) (7H)
**목표:** 컨테이너를 “운영 단위”로 다룰 수 있게 만들기

- PID 1, signal, graceful shutdown
- 리소스 제한: CPU/Memory, OOM, `docker stats`
- `ENTRYPOINT` vs `CMD`, override 패턴
- bind mount vs volume
- 장애 유도 → 원인 분석(메모리/프로세스/포트 충돌)

➡️ 실습: `labs/day02/README.md`

---

## Day 3 — Docker 이미지(기초) & Dockerfile 작성 (7H)
**목표:** Dockerfile로 재현 가능한 빌드 파이프라인 만들기

- 이미지 구조: 레이어/캐시, tag vs digest
- Dockerfile 핵심: `FROM/RUN/COPY/WORKDIR/ENV/EXPOSE/USER`
- `.dockerignore` 전략
- 베이스 이미지 선택: alpine vs debian/ubuntu vs distroless
- 실습: Hello API 이미지 제작 (Node/Python/Java 중 택1)

➡️ 실습: `labs/day03/README.md`

---

## Day 4 — 이미지 최적화 & 멀티스테이지 빌드 (7H)
**목표:** “가볍고 안전한” 운영 이미지 만들기

- 레이어 최적화 원칙
- 멀티스테이지 빌드: build stage/runtime stage 분리
- 레지스트리 push/pull, 태그 전략
- (선택) Trivy 스캔 개요/실습
- 과제: 일반 vs 멀티스테이지 비교 리포트

➡️ 실습: `labs/day04/README.md`

---

## Day 5 — Docker 네트워킹(운영 필수) (7H)
**목표:** 서비스 간 통신/포트/네트워크 분리 이해

- 네트워크 드라이버: bridge/host/none
- 사용자 정의 네트워크 + DNS(Service discovery)
- 실습: 2-tier/3-tier 구성(web↔api↔db)
- 트러블슈팅: 포트 충돌, 0.0.0.0, 방화벽
- 과제: 내부 통신만 허용 설계 + compose 초안

➡️ 실습: `labs/day05/README.md`

---

## Day 6 — 스토리지(Volume/Bind) & 데이터 영속성 (7H)
**목표:** “데이터는 컨테이너 밖에 둔다” 원칙 체득

- bind mount vs volume vs tmpfs
- DB 컨테이너 운영: 초기 스키마/seed, 백업/복구
- UID/GID, 권한 이슈(특히 Windows/WSL)
- 운영 팁: 로그/데이터 분리
- 과제: 백업→삭제→복구 자동화

➡️ 실습: `labs/day06/README.md`

---

## Day 7 — Docker Compose(기초→실전) (7H)
**목표:** 로컬/개발 환경을 Compose로 표준화

- compose.yml: services/ports/volumes/networks
- 실습: 3-tier compose 구성
- depends_on, healthcheck, restart, profiles, env_file
- dev/prod 분리(override 전략)
- 과제: profiles로 dev/prod 스위칭

➡️ 실습: `labs/day07/README.md`

---

## Day 8 — Docker 데몬 & 디버깅(장애 대응) (7H)
**목표:** “안 뜬다/느리다/끊긴다”를 스스로 진단

- daemon/containerd/runc 개요
- `logs/inspect/events/top/stats` 디버깅
- 네트워크/스토리지 장애 케이스
- 실습: 장애 시나리오 5종 → Runbook 작성

➡️ 실습: `labs/day08/README.md`

---

## Day 9 — Jenkins CI로 Docker 빌드/배포 자동화 (7H)
**목표:** “빌드→테스트→푸시” CI 흐름 구현

- Jenkins + Docker 연동, socket mount 보안 주의
- Jenkinsfile 구조, stage, credentials
- 실습: Git clone → test → build → tag → push
- 버전/태깅 전략(semver, git sha)
- 과제: 브랜치/PR 태그 분리 규칙

➡️ 실습: `labs/day09/README.md`

---

## Day 10 — 캡스톤 & 운영 베스트프랙티스 (7H)
**목표:** 작은 서비스라도 “운영 가능한 컨테이너 시스템”으로 마무리

- 보안/운영 베스트프랙티스(최소권한, 로그, 취약점 루틴)
- 캡스톤 4H: 3서비스 + Compose + 멀티스테이지 + Jenkins CI + Runbook
- 발표/리뷰 + 최종 체크리스트

➡️ 캡스톤: `capstone/README.md`
