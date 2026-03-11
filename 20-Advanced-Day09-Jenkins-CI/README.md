# Day 09 — Jenkins CI로 Docker 빌드/푸시

## 목표
- Jenkinsfile로 빌드→테스트→푸시 파이프라인을 만든다.
- 태깅 전략을 적용한다.

## 진행(권장)
- 30m: Jenkins+Docker 연동
- 120m: Pipeline 기초
- 180m: 실습(빌드/푸시)
- 60m: 태그 전략
- 30m: 리뷰

## 실습
### Lab) Jenkinsfile 적용
- `../_shared-advanced-core/templates/Jenkinsfile` 참고
- credentialsId: `dockerhub` (username/password) 등록
- stages: checkout → test → build → login → push

### 체크 포인트
- 빌드 실패 시 로그에서 원인 찾기
- 브랜치별 TAG 정책 적용


## 과제
- 과제: 브랜치/PR 태그 규칙 설계 및 Jenkinsfile에 반영


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
