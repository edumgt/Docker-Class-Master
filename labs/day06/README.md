# Day 06 — 스토리지(볼륨/백업/복구)

## 목표
- DB 컨테이너에서 데이터 영속성을 구성한다.
- 백업→삭제→복구 흐름을 자동화한다.

## 진행(권장)
- 30m: 스토리지 개념
- 150m: DB 볼륨 실습
- 120m: 백업/복구
- 60m: 권한 이슈
- 60m: 리뷰

## 실습
### Lab) Postgres 백업/복구 예시
- 볼륨 생성: `docker volume create pgdata`
- 실행: `docker run -d --name pg -e POSTGRES_PASSWORD=app -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres:16-alpine`
- 백업: `docker exec -t pg pg_dumpall -c -U postgres > backup.sql`
- 삭제: `docker rm -f pg`
- 복구: 새 컨테이너 실행 후 `cat backup.sql | docker exec -i pg psql -U postgres`


## 과제
- 과제: 백업/복구 스크립트(sh 또는 ps1) 작성 + README 정리


## 체크리스트
- [ ] 명령어/결과를 README에 기록했다
- [ ] 실패/오류 상황을 1개 이상 재현하고 해결했다
- [ ] “왜 이런 결과가 나왔는지”를 한 줄로 설명할 수 있다
