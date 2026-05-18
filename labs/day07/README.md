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
- `cp templates/docker-compose.yml docker-compose.yml`
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
