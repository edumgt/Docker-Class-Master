# Docker 소개

## Docker 소개
- 전통적인 인프라에서 어떤 문제가 있었나요?
- 왜 Docker를 사용해야 하나요?
- Docker의 장점은 무엇인가요?
- 소개 자료는 [메인 커리큘럼 문서](../README.md)를 참고하세요.

# Docker 아키텍처

## Docker 아키텍처와 용어 이해
- Docker 데몬(Docker Daemon)이란?
- Docker 클라이언트(Docker Client)란?
- Docker 이미지(Docker Image)란?
- Docker 컨테이너(Docker Container)란?
- Docker 레지스트리/허브(Docker Registry/Docker Hub)란?
- 자세한 내용은 [메인 커리큘럼 문서](../README.md)를 참고하세요.

---

## 수업 보강 가이드
<!-- course-boost-foundation-v1 -->

### 학습 목표(보강)
- Docker CLI를 단순 암기하지 않고, "이미지/컨테이너/볼륨/네트워크"의 관계로 설명할 수 있다.
- 동일 실습을 `run` 단건 명령과 `compose` 방식으로 모두 재현할 수 있다.
- 장애가 났을 때 `logs`, `inspect`, `exec`로 원인을 1차 분석할 수 있다.

### 실습 전 체크리스트
- `docker version` / `docker info`가 정상 출력되는지 확인
- 로컬에 사용 가능한 디스크 여유 10GB 이상 확보
- 포트 충돌 확인: `80`, `443`, `8080`, `3306`, `5432`

### 수업 운영(권장)
1. 개념 설명 20분: 컨테이너와 VM의 차이, 레이어/캐시 개념
2. 데모 20분: 강사가 명령 실행 후 결과 해석 시연
3. 실습 60분: 학습자 직접 실행 + 체크포인트 제출
4. 회고 20분: 실패 사례 공유, 재현 가능한 명령 정리

### 제출물(권장)
- 실행 명령 히스토리(중요 명령 10개 이상)
- `docker ps -a`, `docker images` 결과 캡처
- 장애 1건 이상 재현 + 해결 과정(runbook 10줄 이상)

### 평가 포인트
- 명령 실행 자체보다 "왜 이 명령을 썼는지" 설명 가능한지
- 동일 결과를 다른 방법(run/compose)으로 재현 가능한지
- 정리 문서에 복구 절차가 포함되어 있는지
