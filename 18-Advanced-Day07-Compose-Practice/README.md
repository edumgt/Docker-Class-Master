# Day 07 — Docker Compose 실전

## 목표
- compose로 멀티서비스 환경을 표준화한다.
- healthcheck/profiles로 dev/prod 구성을 분리한다.

## 진행(권장)
- 30m: compose 기본
- 150m: 3-tier compose
- 120m: healthcheck/profiles
- 60m: dev/prod 분리
- 60m: 리뷰

## 실습
### Lab) compose 실행
- `cp ../_shared-advanced-core/templates/docker-compose.yml docker-compose.yml`
- `docker compose up -d`
- `docker compose ps`
- `docker compose logs -f`

### 확장: healthcheck 추가
- db healthcheck 추가 후 `depends_on` 조건 활용(가능한 범위에서)


## 과제
- 과제: dev/prod profiles 구성(예: dev는 포트 노출, prod는 내부만) + 실행 방법 문서화


## 체크리스트
- [ ] 명령어/결과를 README에 기록했다
- [ ] 실패/오류 상황을 1개 이상 재현하고 해결했다
- [ ] “왜 이런 결과가 나왔는지”를 한 줄로 설명할 수 있다

---

## 수업 보강 가이드 (강의자/학습자 공용)
<!-- course-boost-advanced-v1 -->

### 사전 준비
- 실습 시작 전 `docker system df`로 디스크 사용량 점검
- 각 실습 폴더에서 `docker compose config`로 문법 검증
- 포트 충돌 시 기존 컨테이너 정리: `docker ps -a` -> `docker rm -f <name>`

### 제출물 표준
- `README` 체크리스트 완료 여부
- 실행 로그(핵심 명령 + 결과)
- 실패 사례 1건 이상 + 원인/해결/재발방지

### 평가 루브릭(권장)
- 정확성: 명령/설정이 요구사항과 일치하는가
- 재현성: 다른 환경에서 다시 실행 가능한가
- 설명력: 의사결정 이유(이미지/네트워크/볼륨 선택)가 명확한가

### 심화 미션
1. 같은 실습을 "수동 명령"과 "compose 자동화" 두 방식으로 재작성
2. `Makefile` 또는 셸 스크립트로 start/stop/log/clean 명령 래핑
3. 팀 기준 runbook(장애 조치 절차) 1페이지 작성
