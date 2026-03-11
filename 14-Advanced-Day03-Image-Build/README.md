# Day 03 — 이미지 기초 & Dockerfile 작성

## 목표
- Dockerfile로 애플리케이션 이미지를 만든다.
- 레이어/캐시 개념을 이해하고 `.dockerignore`를 적용한다.

## 진행(권장)
- 30m: 이미지 구조
- 90m: Dockerfile 문법
- 120m: 실습(Hello API)
- 90m: 캐시 최적화
- 90m: 리뷰/정리

## 실습
### Lab) Hello API 이미지 만들기(예: Node)
1) `../_shared-advanced-core/templates/Dockerfile.node` 참고하여 Dockerfile 작성
2) `docker build -t hello-api:dev .`
3) `docker run --rm -p 3000:3000 hello-api:dev`

### 체크 포인트
- `docker image ls`에서 용량 확인
- `docker history hello-api:dev`로 레이어 확인


## 과제
- 과제: 캐시 최적화 전/후 빌드 시간 및 이미지 크기 비교 리포트 작성


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
