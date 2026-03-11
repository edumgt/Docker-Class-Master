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
