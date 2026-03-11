# Docker Fundamentals & On-Prem DevSecOps Lab

> Docker 기본 학습(1~5), 온프레미스 DevSecOps 연동(6~11), 확장 실습(12~13)까지 한 흐름으로 실습하는 통합 레포지토리

> [!NOTE]
> 이 문서는 기존 메인 안내/운영 가이드를 병합해 정리한 통합 문서입니다.

## 목차
- [1. 학습 로드맵](#1-학습-로드맵)
- [2. Docker Desktop 빠른 제어](#2-docker-desktop-빠른-제어)
- [3. 아키텍처 개요](#3-아키텍처-개요)
- [4. 온프렘 최소 자원 산정](#4-온프렘-최소-자원-산정)
- [5. 운영 고도화 확장 스택](#5-운영-고도화-확장-스택)
- [6. 통합 의존관계 다이어그램](#6-통합-의존관계-다이어그램)
- [7. WSL 포트 80 트러블슈팅](#7-wsl-포트-80-트러블슈팅)
- [8. Docker 이미지 목록](#8-docker-이미지-목록)
- [9. 대상 독자와 도입 로드맵](#9-대상-독자와-도입-로드맵)
- [10. 12번 폴더: OnPrem ERP 파트](#10-12번-폴더-onprem-erp-파트)
- [11. 13번 폴더: Advanced 파트](#11-13번-폴더-advanced-파트)

---

## 1. 학습 로드맵

| 단계 | 주제 | 이동 |
|---|---|---|
| 01 | Docker 소개 | [01-Docker-Introduction](./01-Docker-Introduction/README.md) |
| 02 | Docker 설치 | [02-Docker-Installation](./02-Docker-Installation/README.md) |
| 03 | Docker Hub 이미지 Pull/Run | [03-Pull-from-DockerHub-and-Run-Docker-Images](./03-Pull-from-DockerHub-and-Run-Docker-Images/README.md) |
| 04 | 이미지 Build/Run/Push | [04-Build-new-Docker-Image-and-Run-and-Push-to-DockerHub](./04-Build-new-Docker-Image-and-Run-and-Push-to-DockerHub/README.md) |
| 05 | 핵심 Docker 명령어 | [05-Essential-Docker-Commands](./05-Essential-Docker-Commands/README.md) |
| 06 | Jenkins 온프레미스 구축 | [06-Jenkins-Server-On-Prem](./06-Jenkins-Server-On-Prem/README.md) |
| 07 | GitLab CE 온프레미스 구축 | [07-GitLab-CE-On-Prem](./07-GitLab-CE-On-Prem/README.md) |
| 08 | SonarQube 온프레미스 구축 | [08-SonarQube-On-Prem](./08-SonarQube-On-Prem/README.md) |
| 09 | Nexus Repository 온프레미스 구축 | [09-Nexus-Repository-On-Prem](./09-Nexus-Repository-On-Prem/README.md) |
| 10 | Drone CI 온프레미스 구축 | [10-Drone-CI-On-Prem](./10-Drone-CI-On-Prem/README.md) |
| 11 | 통합 DevSecOps Lab | [11-Integrated-DevSecOps-Lab](./11-Integrated-DevSecOps-Lab/README.md) |
| 12 | OnPrem ERP 통합 실습 | [12-Docker-OnPrem-ERP](./12-Docker-OnPrem-ERP/README.md) |
| 13 | Docker Advanced Example 실습 | [13-Docker-Advanced-Example](./13-Docker-Advanced-Example/README.md) |

---

## 2. Docker Desktop 빠른 제어

### CLI
```bash
# 상태 확인 (4.37+)
docker desktop status

# 시작 / 재시작 / 중지
docker desktop start
docker desktop restart
docker desktop stop

# 로그 확인
docker desktop logs
```

### PowerShell
```powershell
# Docker Desktop 관련 프로세스 종료
Get-Process "*docker*" -ErrorAction SilentlyContinue | Stop-Process -Force

# Docker Desktop UI 재실행
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

---

## 3. 아키텍처 개요

### 핵심 플랫폼 레이어
| 레이어 | 구성 요소 |
|---|---|
| Container Runtime | Docker Engine |
| SCM | GitLab CE |
| CI | Jenkins, Drone CI |
| Quality Gate | SonarQube |
| Artifact Registry | Nexus Repository OSS (또는 Docker Hub/Harbor) |
| Runtime Workload | Nginx, Spring Boot 등 |

### 표준 흐름 (Reference Flow)
1. 개발자가 GitLab CE에 코드 Push
2. Jenkins 또는 Drone CI 파이프라인 실행
3. SonarQube 품질 검사 수행
4. Docker 이미지 빌드 후 Nexus(또는 Docker Hub)로 Push
5. 운영 노드가 이미지 Pull 후 배포

> [!TIP]
> 기본 체인은 `GitLab -> Jenkins/Drone -> SonarQube -> Nexus -> Docker Runtime` 으로 이해하면 됩니다.

### 권장 네트워크 존
- `Zone 1 (Dev)`: 개발자 PC, 로컬 Docker
- `Zone 2 (CI)`: GitLab, Jenkins/Drone, SonarQube
- `Zone 3 (Artifact)`: Nexus/Harbor
- `Zone 4 (Runtime)`: 서비스 컨테이너 실행 노드
- `Zone 5 (Ops)`: 모니터링, 로깅, 백업, 보안

권장 정책:
- CI Zone -> Artifact Zone: Push 허용
- Runtime Zone -> Artifact Zone: Pull 허용
- Dev Zone -> Runtime Zone: 직접 접근 제한

---

## 4. 온프렘 최소 자원 산정

> [!IMPORTANT]
> 아래 수치는 단일 노드 실습/PoC 최소 기준입니다. 운영 환경은 최소 1.5~2배 여유 자원을 권장합니다.

### 기준 범위
- 06~10장: Jenkins, GitLab CE, SonarQube, Nexus, Drone
- 11장: Integrated DevSecOps Lab (`docker-compose.yml`) 기본/선택 프로파일
- 기준 파일:
  - `06-Jenkins-Server-On-Prem/Dockerfile`
  - `07-GitLab-CE-On-Prem/Dockerfile`
  - `08-SonarQube-On-Prem/Dockerfile`
  - `09-Nexus-Repository-On-Prem/Dockerfile`
  - `10-Drone-CI-On-Prem/Dockerfile`
  - `11-Integrated-DevSecOps-Lab/docker-compose.yml`

### 이미지별 최소 컴퓨팅 자원
| 구분 | Docker 이미지 | 최소 vCPU | 최소 RAM | 최소 디스크(볼륨) | 비고 |
|---|---|---:|---:|---:|---|
| CI | `jenkins/jenkins:lts-jdk17` | 2 | 4 GB | 50 GB | 플러그인/워크스페이스 증가 고려 |
| SCM | `gitlab/gitlab-ce:17.5.2-ce.0` | 4 | 8 GB | 100 GB | 실무 최소 여유 반영 |
| Code Quality | `sonarqube:community` | 2 | 4 GB | 50 GB | 운영은 외부 PostgreSQL 연동 권장 |
| Artifact | `sonatype/nexus3:3.70.1` | 2 | 4 GB | 100 GB | Blob 저장 증가 유의 |
| CI (경량) | `drone/drone:2` | 1 | 1 GB | 20 GB | Runner 별도 산정 필요 |
| Reverse Proxy | `traefik:v3.1` | 1 | 1 GB | 10 GB | 인증서/액세스 로그 포함 |
| DB | `postgres:16` | 1 | 2 GB | 20 GB | Keycloak 백엔드 DB |
| IAM | `quay.io/keycloak/keycloak:25.0.5` | 1 | 2 GB | 10 GB | 사용자 증가 시 확장 필요 |
| Secrets | `hashicorp/vault:1.17` | 1 | 1 GB | 10 GB | 레포는 Dev 모드 |
| Scanner | `aquasec/trivy:0.56.2` | 1 | 1 GB | 10 GB | 스캔 시 순간 부하 증가 |
| Metrics | `prom/prometheus:v2.54.1` | 2 | 2 GB | 30 GB | 보관 기간에 비례해 디스크 증가 |
| Alert | `prom/alertmanager:v0.27.0` | 1 | 1 GB | 5 GB | 알림 라우팅 |
| Dashboard | `grafana/grafana:11.2.2` | 1 | 1 GB | 10 GB | 대시보드/플러그인 저장 |
| Logs | `grafana/loki:3.1.1` | 2 | 2 GB | 30 GB | 로그 보관 정책 핵심 |
| Log Agent | `grafana/promtail:3.1.1` | 1 | 1 GB | 5 GB | 호스트 로그 수집 |
| Private CA (옵션) | `smallstep/step-ca:0.27.4` | 1 | 1 GB | 5 GB | `private-ca` profile |
| Harbor DB (옵션) | `goharbor/harbor-db:v2.11.1` | 1 | 2 GB | 20 GB | `harbor` profile |
| Harbor Redis (옵션) | `goharbor/redis-photon:v2.11.1` | 1 | 1 GB | 10 GB | `harbor` profile |
| Harbor Registry (옵션) | `goharbor/registry-photon:v2.11.1` | 2 | 2 GB | 80 GB | `harbor` profile |

### 합산 최소 사양 (단일 노드)
| 시나리오 | 최소 vCPU 합계 | 최소 RAM 합계 | 최소 디스크 합계 |
|---|---:|---:|---:|
| 06~10장 핵심 스택 (Jenkins+GitLab+Sonar+Nexus+Drone) | 11 | 21 GB | 320 GB |
| 11장 기본 프로파일 (Traefik~Promtail) | 12 | 14 GB | 140 GB |
| 11장 + `private-ca` + `harbor` 프로파일 | 17 | 20 GB | 255 GB |

추가 권장 오버헤드: `2 vCPU`, `4 GB RAM`, `30 GB` (호스트 OS + Docker)

---

## 5. 운영 고도화 확장 스택

### 보안/접근제어
- Keycloak: SSO 및 중앙 인증
- HashiCorp Vault: 비밀정보 중앙관리
- Trivy: 이미지 취약점 스캔 자동화

### 관측성
- Prometheus + Grafana: 메트릭/대시보드
- Loki + Promtail (또는 EFK/ELK): 로그 수집/분석
- Alertmanager: 알림 자동화

### 네트워크/트래픽
- Traefik / Nginx Proxy Manager: 리버스 프록시, TLS 종료
- 사설 CA 기반 인증서 운영 전략 수립

### 이미지 거버넌스
- Harbor: 내부 레지스트리 + 취약점 스캔 + 정책
- Nexus와 병행 또는 대체 가능

### 백업/DR
- GitLab, SonarQube, Nexus 볼륨/DB 정기 백업
- MinIO 등 오브젝트 스토리지 기반 보관

---

## 6. 통합 의존관계 다이어그램

```mermaid
flowchart LR
  subgraph Core["06~10 Core On-Prem Stack"]
    DEV[Developer]
    GITLAB["gitlab/gitlab-ce"]
    JENKINS["jenkins/jenkins"]
    DRONE["drone/drone"]
    SONAR["sonarqube:community"]
    NEXUS["sonatype/nexus3"]
    RUNTIME[Docker Runtime Host]

    DEV -->|Push| GITLAB
    GITLAB -->|Webhook/Trigger| JENKINS
    GITLAB -->|Webhook/Trigger| DRONE
    JENKINS -->|Quality Scan| SONAR
    DRONE -->|Quality Scan| SONAR
    JENKINS -->|Build/Push Image| NEXUS
    DRONE -->|Build/Push Image| NEXUS
    RUNTIME -->|Pull Image| NEXUS
  end

  subgraph Lab["11 Integrated DevSecOps Lab"]
    TRAEFIK["traefik:v3.1"]
    POSTGRES["postgres:16"]
    KEYCLOAK["keycloak:25.0.5"]
    VAULT["vault:1.17"]
    TRIVY["trivy:0.56.2"]
    PROM["prometheus:v2.54.1"]
    ALERT["alertmanager:v0.27.0"]
    GRAFANA["grafana:11.2.2"]
    LOKI["loki:3.1.1"]
    PROMTAIL["promtail:3.1.1"]
    STEPCA["step-ca:0.27.4 (profile)"]
    HDB["harbor-db:v2.11.1 (profile)"]
    HREDIS["harbor-redis:v2.11.1 (profile)"]
    HREG["harbor-registry:v2.11.1 (profile)"]

    KEYCLOAK -->|DB| POSTGRES
    GRAFANA -->|Query Metrics| PROM
    GRAFANA -->|Query Logs| LOKI
    PROMTAIL -->|Ship Logs| LOKI
    PROM -->|Alert Route| ALERT

    TRAEFIK -->|Route| KEYCLOAK
    TRAEFIK -->|Route| VAULT
    TRAEFIK -->|Route| PROM
    TRAEFIK -->|Route| GRAFANA
    TRAEFIK -->|Route| HREG

    HREG -->|Metadata/State| HDB
    HREG -->|Cache/Queue| HREDIS
    STEPCA -->|Internal TLS (optional)| TRAEFIK
    TRIVY -->|Image Scan Target| HREG
  end
```

산정 가정:
- 단일 Docker Host 최소 실습 기준
- HA/장기보관/대규모 부하는 미반영
- 디스크는 GitLab/SonarQube/Nexus부터 우선 확장 고려

---

## 7. WSL 포트 80 트러블슈팅

### 1) 점유 프로세스 확인
```bash
# LISTEN 중인 80 포트 프로세스
sudo ss -ltnp 'sport = :80'

# 프로세스/사용자/FD 상세 확인
sudo lsof -iTCP:80 -sTCP:LISTEN -n -P
```

### 2) 점유 프로세스 종료
```bash
# 방법 A: 서비스 종료 (예: nginx)
sudo systemctl stop nginx 2>/dev/null || sudo service nginx stop

# 방법 B: PID 강제 종료 (예시)
sudo kill -9 197
```

### 3) 해제 확인
```bash
sudo ss -ltnp 'sport = :80'
```

> [!WARNING]
> `kill -9`는 마지막 수단으로만 사용하고, 가능하면 서비스 정상 종료를 우선 사용하세요.

---

## 8. Docker 이미지 목록

| 애플리케이션 | Docker 이미지 |
|---|---|
| Nginx | `nginx` |
| 커스텀 Nginx | `stacksimplify/mynginx_image1` |
| Spring Boot HelloWorld | `stacksimplify/dockerintro-springboot-helloworld-rest-api` |
| Jenkins LTS | `jenkins/jenkins:lts-jdk17` |
| GitLab CE | `gitlab/gitlab-ce:17.5.2-ce.0` |
| SonarQube Community | `sonarqube:community` |
| Nexus Repository OSS | `sonatype/nexus3:3.70.1` |
| Drone CI | `drone/drone:2` |

---

## 9. 대상 독자와 도입 로드맵

### 활용 대상
- Docker를 처음 학습하는 엔지니어
- 온프레미스 DevOps/Platform 구축을 시작하는 팀
- 도구 간 연결 구조를 빠르게 파악하려는 Solution Architect

### 단계별 도입
1. **Phase 1 (기본기/PoC)**
   - 1~10 단계 실습 완료
   - Jenkins/Drone 중 표준 CI 1개 선정
2. **Phase 2 (표준화)**
   - 브랜치 전략, 파이프라인 템플릿, Sonar 품질 게이트 표준화
   - Nexus 저장소 구조(팀/환경별) 정리
3. **Phase 3 (운영 안정화)**
   - 모니터링/로그/알림 연계
   - 백업/복구 리허설 및 장애 대응 Runbook 작성
4. **Phase 4 (보안 고도화)**
   - SSO, 비밀정보 중앙관리, 이미지 스캔/서명 정책 도입

---

## 10. 12번 폴더: OnPrem ERP 파트

`https://github.com/edumgt/Docker-OnPrem-ERP.git`의 전체 내용을 아래 경로로 병합했습니다.

- `12-Docker-OnPrem-ERP/`
- 시작 문서: `12-Docker-OnPrem-ERP/README.md`
- 주요 실행 파일: `12-Docker-OnPrem-ERP/start.sh`, `12-Docker-OnPrem-ERP/stop.sh`, `12-Docker-OnPrem-ERP/docker-compose.yml`

---

## 11. 13번 폴더: Advanced 파트

`https://github.com/edumgt/Docker-Advanced-Example.git`의 전체 내용을 아래 경로로 병합했습니다.

- `13-Docker-Advanced-Example/`
- 시작 문서: `13-Docker-Advanced-Example/README.md`
- 주요 파일: `13-Docker-Advanced-Example/docker-compose.yml`, `13-Docker-Advanced-Example/labs/`, `13-Docker-Advanced-Example/docs/`
