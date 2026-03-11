# Day 01 — Docker 개요 & 컨테이너 첫 걸음

## 목표
- Docker 핵심 개념(이미지/컨테이너/레지스트리)을 이해한다.
- 기본 CLI로 컨테이너를 실행/중지/삭제/로그확인 할 수 있다.

## 진행(권장)
- 20m: 개념(컨테이너 vs VM)
- 60m: 설치/환경 점검
- 120m: 기본 CLI 실습
- 120m: 미니랩(nginx)
- 60m: 리뷰/정리

## 실습
### Lab 1) 설치/점검
- `docker version`
- `docker info`

### Lab 2) run/ps/stop/rm
- `docker run --name hello -d nginx:alpine`
- `docker ps`
- `docker logs hello`
- `docker stop hello`
- `docker rm hello`

### Lab 3) 포트 바인딩
- `docker run --name web -d -p 8080:80 nginx:alpine`
- 브라우저로 `http://localhost:8080` 확인
- `docker logs -f web` (접속 로그 확인)

### Lab 4) exec/cp
- `docker exec -it web sh`
- (컨테이너 내부) `ls -al /usr/share/nginx/html`
- `docker cp web:/usr/share/nginx/html/index.html ./index.html`


## 과제
- 과제1: 컨테이너 3종 실행 스크립트 작성(nginx/redis/busybox)
- 과제2: `docker ps -a`로 남은 리소스 정리 순서 문서화


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
