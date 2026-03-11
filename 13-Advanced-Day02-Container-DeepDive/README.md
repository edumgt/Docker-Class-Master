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
