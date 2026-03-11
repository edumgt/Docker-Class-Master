# Docker 설치

## Docker 설치 가이드
- https://docs.docker.com/install/

![alt text](image.png)

## Windows용 Docker Desktop
- https://docs.docker.com/docker-for-windows/

## Mac용 Docker Desktop
- https://docs.docker.com/docker-for-mac/

### Mac에서 Docker Desktop 문제 해결 (osxkeychain)
- Mac에서 **osxkeychain** 관련 문제가 발생할 수 있습니다.
- 아래 단계를 따라 해결합니다.
- **사전 참고 자료:**
  - https://medium.com/@dakshika/error-creating-the-docker-image-on-macos-wso2-enterprise-integrator-tooling-dfb5b537b44e

**Step 1: Docker Desktop 설정 변경**
- Docker Desktop → Preferences를 엽니다.
- **Securely store Docker logins in macOS keychain** 옵션을 해제합니다.

**Step 2: config.json 수정**
- **.docker** 폴더의 **config.json** 파일을 엽니다.
- 예시 경로:
  - /Users/<userid>/.docker/config.json
  - ~/.docker/config.json
- config.json에서 **"credSstore": "osxkeychain"** 라인을 제거합니다.

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
