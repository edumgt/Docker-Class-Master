# 10장 - Drone CI 온프레미스 구축 (Dockerfile 기반)

## Drone CI 소개
Drone CI는 컨테이너 기반 파이프라인을 간결하게 구성할 수 있는 오픈소스 CI/CD 도구입니다.
`.drone.yml` 선언형 파이프라인으로 빌드/테스트/배포 단계를 빠르게 자동화할 수 있습니다.

---

# Drone (오픈소스 CI/CD) 정리

> 여기서 말하는 **Drone**은 “하늘 나는 드론”이 아니라, Git 이벤트(푸시/PR 등)를 트리거로 **빌드·테스트·배포 파이프라인을 자동 실행**하는 **오픈소스 CI/CD 도구(Drone CI / Drone.io)** 입니다.

---

## 1) Drone CI 한 줄 정의
- **리포지토리 안의 `.drone.yml`** 파일로 파이프라인을 정의하고
- **Runner(실행기)** 가 각 step을 **컨테이너 기반**으로 실행하는 CI/CD 시스템

---

## 2) 구성 요소(아키텍처 관점)
- **VCS 연동(GitHub/GitLab 등)**  
  - Push/PR/Webhook 이벤트가 발생하면 Drone이 이를 받음
- **Drone Server**
  - 리포지토리의 `.drone.yml` 파이프라인을 읽고 실행을 오케스트레이션
  - 결과(성공/실패)를 다시 VCS에 상태로 남김
- **Drone Runner**
  - 실제 빌드/테스트/배포 작업을 수행
  - 실행 방식에 따라 (예: Docker runner / Kubernetes runner 등) 운영 형태가 달라짐

---

## 3) 동작 흐름(End-to-End)
1. 개발자가 **push / PR** 생성  
2. Git 서버가 **Webhook** 으로 Drone Server에 이벤트 전달  
3. Drone Server가 리포의 **`.drone.yml`** 을 로드  
4. Runner가 step을 순서대로 실행 (대부분 **컨테이너 단위**)  
5. 성공/실패 결과를 Git 서버의 **상태 체크(Status Check)** 로 반영

---

## 4) `.drone.yml` 기본 구조
Drone 파이프라인 파일은 보통 아래 형태로 시작합니다.

- `kind: pipeline` : 파이프라인 정의
- `type:` : 실행 환경(예: docker)
- `name:` : 파이프라인 이름
- `steps:` : 단계 목록(각 step은 이미지 + 명령어)

---

## 5) 예제 1 — Node.js 테스트 + 빌드
```yaml
kind: pipeline
type: docker
name: default

steps:
  - name: test
    image: node:20
    commands:
      - npm ci
      - npm test

  - name: build
    image: node:20
    commands:
      - npm run build
```

---

## 6) 예제 2 — Docker 이미지 빌드/푸시(개념 예시)
> 아래는 “어떤 식으로 구성하는지”를 보여주는 개념 예시입니다.  
> 실제로는 Registry 인증(Secrets), 태그 전략, 브랜치 조건 등을 추가합니다.

```yaml
kind: pipeline
type: docker
name: build-and-push

steps:
  - name: docker-build
    image: docker:26
    volumes:
      - name: dockersock
        path: /var/run/docker.sock
    commands:
      - docker build -t my-registry.local/myapp:${DRONE_COMMIT_SHA} .

  - name: docker-push
    image: docker:26
    volumes:
      - name: dockersock
        path: /var/run/docker.sock
    commands:
      - docker push my-registry.local/myapp:${DRONE_COMMIT_SHA}

volumes:
  - name: dockersock
    host:
      path: /var/run/docker.sock
```

---

## 7) 장점 요약
- **파이프라인이 리포 안에 있어** 버전 관리/재현이 쉬움
- **컨테이너 기반 step 실행**으로 환경 불일치로 인한 실패를 줄이기 좋음
- 다양한 플러그인/템플릿을 컨테이너로 구성 가능

---

## 8) 운영 시 체크 포인트
- **Runner 실행 방식 선택**
  - Docker 기반: 구성 단순, 빠른 시작
  - Kubernetes 기반: 클러스터에서 확장/격리/리소스 관리가 쉬움
- **Secrets 관리**
  - Registry 계정, 배포 키, API 토큰 등은 코드에 직접 박지 말고 Secrets로 분리
- **태그/브랜치 전략**
  - main 브랜치만 배포, PR은 테스트만 등 조건을 명확히
- **폐쇄망(온프레미스)**
  - 내부 Registry(Harbor 등)와 연계, 외부 이미지 의존 최소화(미러링/캐시)

---

## 9) Jenkins / GitHub Actions와 비교(감 잡기)
- Drone: **컨테이너 네이티브 + `.drone.yml` 중심**  
- Jenkins: 플러그인 생태계 강력, 자유도 높지만 운영 복잡도 증가 가능
- GitHub Actions: GitHub에 밀착(편리), 온프레/폐쇄망은 제약이 있을 수 있음

---

## 10) 다음 단계(원하면 바로 이어서)
원하시면 아래 중 한 가지 목표를 기준으로 **실제 적용 템플릿**까지 만들어 드릴게요.

- (A) **폐쇄망 + Harbor 레지스트리 + Docker runner** 기반 배포
- (B) **Kubernetes runner**로 클러스터 내부 배포(GitOps/Helm 연계)
- (C) 기존 **GitHub Actions/CodeBuild/Jenkins**에서 Drone으로 전환 가이드

---

## 참고 링크
- Drone 공식: https://www.drone.io/
- Drone Docs: https://docs.drone.io/

---

## 이 장의 목표
- Dockerfile 기반 Drone 서버 이미지 구성
- 온프레미스에서 경량 CI 서버 실행
- GitHub/Gitea/GitLab OAuth 연동을 위한 기본 환경 변수 확인

## Dockerfile
```dockerfile
FROM drone/drone:2

ENV DRONE_SERVER_HOST=drone.local \
    DRONE_SERVER_PROTO=http \
    DRONE_RPC_SECRET=change-me

EXPOSE 80
```

### 구성 포인트
- `drone/drone:2` 공식 이미지 사용
- `DRONE_RPC_SECRET`: Drone 서버/러너 인증에 필수
- 실제 운영 시 OAuth 관련 ENV는 외부 주입 권장

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-drone:1.0 .

# 2) 볼륨 생성
docker volume create drone_data

# 3) 컨테이너 실행
docker run -d --name drone-server \
  -p 8083:80 \
  -v drone_data:/data \
  -e DRONE_GITEA_SERVER=http://gitea.local \
  -e DRONE_GITEA_CLIENT_ID=your-client-id \
  -e DRONE_GITEA_CLIENT_SECRET=your-client-secret \
  -e DRONE_RPC_SECRET=change-me \
  -e DRONE_USER_CREATE=username:admin,admin:true \
  onprem-drone:1.0
```

## 운영 팁
- Drone Runner는 서버와 분리하여 독립 배포 권장
- `DRONE_RPC_SECRET`는 강력한 랜덤 값으로 교체
- 사내 Git 서버(Gitea/GitLab)와 SSO/OAuth 통합 권장

---

## 수업 보강 가이드
<!-- course-boost-onprem-v1 -->

### 수업 핵심 관점
- 단일 도구 설치가 목표가 아니라, "소스 -> CI -> 품질 -> 아티팩트 -> 배포" 체인을 완성하는 것이 목표입니다.
- 각 도구는 독립 서비스이면서도 네트워크/계정/권한/스토리지 정책으로 강하게 연결됩니다.

### 실습 운영 체크리스트
- 컨테이너 상태: `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`
- 볼륨 상태: `docker volume ls`
- 로그 확인: `docker logs <container> --tail 200`
- 리소스 점검: `docker stats --no-stream`

### 운영 안정화 과제(권장)
1. 컨테이너 재시작 후 데이터 유지 여부 검증
2. 관리자 계정/초기 비밀번호 변경 절차 문서화
3. 백업/복구 테스트(최소 1회)
4. 서비스 헬스체크/장애 알림 조건 정의

### 품질 평가 기준
- 단순 기동이 아니라 "실패 복구"까지 확인했는가
- 파이프라인 실행 기록과 품질 게이트 결과를 남겼는가
- 사내 도입을 가정한 최소 보안 설정(비밀번호/토큰/권한)을 반영했는가

### 다음 단계
- `11-Integrated-DevSecOps-Lab`로 확장하여 인증/시크릿/관측성을 포함한 운영형 실습으로 연결
