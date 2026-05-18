# Day 02 — 컨테이너 심화(프로세스/자원/IO)

## 목표
- PID 1과 시그널 처리 개념을 이해한다.
- 리소스 제한과 OOM 상황을 재현/진단한다.
- bind mount/volume 차이를 실습한다.

## 진행(권장)
- 30m: PID 1/Signal
- 90m: 리소스 제한 실습
- 90m: ENTRYPOINT/CMD
- 150m: 볼륨/마운트
- 60m: 장애 유도/리뷰

## 실습
### Lab 1) 리소스 제한
- `docker run --rm -m 128m --name memtest alpine sh -c "python3 -c 'a="a"*10**8; print(len(a))'"`  
  (환경에 따라 python 없으면 다른 방식으로 메모리 사용 유도)

### Lab 2) restart policy
- `docker run -d --restart=always --name restart-test alpine sh -c "exit 1"`
- `docker ps -a`에서 재시작 여부 확인

### Lab 3) bind mount vs volume
- bind mount: `docker run --rm -v "$(pwd)":/work -w /work alpine ls -al`
- named volume: `docker volume create myvol`
- `docker run --rm -v myvol:/data alpine sh -c "echo hi > /data/hi.txt"`
- `docker run --rm -v myvol:/data alpine cat /data/hi.txt`


## 과제
- 과제: 장애 2종 재현(OOM/포트충돌 등) 후 원인/해결 절차를 md로 작성


## 체크리스트
- [ ] 명령어/결과를 README에 기록했다
- [ ] 실패/오류 상황을 1개 이상 재현하고 해결했다
- [ ] “왜 이런 결과가 나왔는지”를 한 줄로 설명할 수 있다
