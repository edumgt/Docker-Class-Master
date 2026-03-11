## VS Code PDF 뷰어 설치
![alt text](image.png)

# Docker - 핵심 명령어
- 아래는 자주 사용하는 핵심 명령어 목록입니다.

| 명령어 | 설명 |
| --- | --- |
| docker ps | 실행 중인 컨테이너 목록 보기 |
| docker ps -a | 중지/실행 중인 전체 컨테이너 목록 보기 |
| docker stop container-id | 실행 중인 컨테이너 중지 |
| docker start container-id | 중지된 컨테이너 시작 |
| docker restart container-id | 실행 중인 컨테이너 재시작 |
| docker port container-id | 특정 컨테이너의 포트 매핑 확인 |
| docker rm container-id or name | 중지된 컨테이너 삭제 |
| docker rm -f container-id or name | 실행 중인 컨테이너 강제 삭제 |
| docker pull image-info | Docker Hub에서 이미지 Pull |
| docker pull stacksimplify/springboot-helloworld-rest-api:2.0.0-RELEASE | Docker Hub에서 이미지 Pull(예시) |
| docker exec -it container-name /bin/sh | 컨테이너에 접속해 명령 실행 |
| docker rmi image-id | Docker 이미지 삭제 |
| docker logout | Docker Hub 로그아웃 |
| docker login -u username -p password | Docker Hub 로그인 |
| docker stats | 컨테이너 리소스 사용량 실시간 확인 |
| docker top container-id or name | 컨테이너에서 실행 중인 프로세스 확인 |
| docker version | Docker 버전 정보 확인 |

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
