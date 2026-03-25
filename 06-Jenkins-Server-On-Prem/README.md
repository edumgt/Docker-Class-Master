# 06장 - Jenkins 서버 온프레미스 구축 (Dockerfile 기반)

## Jenkins 소개
Jenkins는 가장 널리 사용되는 오픈소스 CI 서버입니다.  
코드 빌드, 테스트, 배포 파이프라인을 자동화하고 수천 개의 플러그인을 통해 다양한 개발 도구와 통합할 수 있습니다.

## 이 장의 목표
- Dockerfile로 Jenkins 컨테이너 이미지를 직접 빌드
- 온프레미스 환경에서 Jenkins 마스터(컨트롤러) 컨테이너 기동
- 기본 포트/볼륨/초기 관리자 비밀번호 확인까지 실습

## Dockerfile
```dockerfile
FROM jenkins/jenkins:latest

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io git curl nginx python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY scripts/sse_log_server.py /usr/local/bin/sse_log_server.py
COPY scripts/start-services.sh /usr/local/bin/start-services.sh
COPY www/install-log.html /usr/share/nginx/html/install-log.html

RUN chmod +x /usr/local/bin/sse_log_server.py /usr/local/bin/start-services.sh \
    && rm -f /etc/nginx/sites-enabled/default \
    && mkdir -p /var/lib/nginx /var/log/nginx /run /var/jenkins_home/logs \
    && chown -R jenkins:jenkins /var/lib/nginx /var/log/nginx /run /var/jenkins_home/logs

USER jenkins
EXPOSE 8888 50000
ENTRYPOINT ["/usr/local/bin/start-services.sh"]
```

### 구성 포인트
- `jenkins/jenkins:latest` 베이스 이미지
- `docker.io`, `git`, `curl`, `nginx`, `python3` 설치
- `8888`: Nginx 리버스 프록시(외부 진입)
- `/sse/events`: Jenkins 시작 로그 SSE 스트리밍 엔드포인트
- `/install-log`: SSE 로그 뷰어 페이지
- `50000`: 에이전트 연결 포트

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-jenkins:1.0 .

# 2) 데이터 보존용 볼륨 생성
docker volume create jenkins_home

# 3) 컨테이너 실행
docker run -d --name jenkins-server \
  -p 8888:8888 -p 50000:50000 \
  --add-host=host.docker.internal:host-gateway \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins:latest
```

## 초기 접속
1. 브라우저에서 `http://localhost:8888` 접속
2. Jenkins 설치 로그 SSE 확인: `http://localhost:8888/install-log`
3. 초기 관리자 비밀번호 확인:
```bash
docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword
```

## 운영 팁
- Jenkins 홈(`/var/jenkins_home`)은 반드시 볼륨으로 분리
- 플러그인 버전은 주기적으로 검증 후 고정 관리
- 운영 환경에서는 리버스 프록시(Nginx) + TLS 적용 권장

## GitLab Push -> Jenkins Trigger -> Docker Nginx 배포 구성

목표:
- GitLab 저장소 `test-gitlab.git`에 push 발생
- Jenkins Pipeline 자동 트리거
- Docker로 Nginx 컨테이너 재배포

### 1) 테스트 저장소 파일 준비
아래 예시 파일을 `test-gitlab.git` 루트에 커밋합니다.
- [examples/test-gitlab-repo/Dockerfile](/home/Docker-Basic/06-Jenkins-Server-On-Prem/examples/test-gitlab-repo/Dockerfile)
- [examples/test-gitlab-repo/index.html](/home/Docker-Basic/06-Jenkins-Server-On-Prem/examples/test-gitlab-repo/index.html)
- [pipelines/Jenkinsfile.gitlab-nginx-deploy](/home/Docker-Basic/06-Jenkins-Server-On-Prem/pipelines/Jenkinsfile.gitlab-nginx-deploy) -> 저장소에서는 파일명을 `Jenkinsfile`로 사용

### 2) Jenkins 플러그인 설치
`Manage Jenkins -> Plugins`:
- `GitLab`
- `Pipeline`
- `Git`

### 3) Jenkins Credential 등록
`Manage Jenkins -> Credentials -> (global)`:
- 타입: `Username with password`
- Username: `root` (또는 GitLab 사용자)
- Password: `GitLab Personal Access Token`
- ID 예시: `gitlab-http-token`

### 4) Jenkins Job 생성 (Pipeline)
`New Item -> Pipeline` (Job 이름 예시: `test-gitlab-nginx-deploy`)

설정:
- `Build Triggers`: `Build when a change is pushed to GitLab. GitLab webhook URL: ...` 체크
- `Pipeline -> Definition`: `Pipeline script from SCM`
- `SCM`: `Git`
- `Repository URL`: `http://host.docker.internal/root/test-gitlab.git`
  - Jenkins 컨테이너 내부에서 `http://localhost/...`는 Jenkins 자신을 가리키므로 사용하지 않습니다.
  - GitLab을 8081 포트로 publish했다면 `http://host.docker.internal:8081/root/test-gitlab.git`를 사용합니다.
  - 같은 Docker network면 `http://gitlab-ce/root/test-gitlab.git`도 사용 가능합니다.
- `Credentials`: `gitlab-http-token`
- `Branch Specifier`: `*/main` (또는 실제 브랜치)
- `Script Path`: `Jenkinsfile`

### 5) GitLab Webhook 설정
GitLab 프로젝트 `test-gitlab`에서:
- `Settings -> Webhooks`
- URL: `http://host.docker.internal:8888/project/test-gitlab-nginx-deploy`
  - GitLab 컨테이너에서 Jenkins로 접근해야 하므로 `localhost` 대신 `host.docker.internal` 또는 Jenkins 컨테이너 DNS 사용
- Trigger: `Push events`
- (선택) Secret token 설정 시 Jenkins Job의 GitLab trigger token과 동일하게 맞춤

`Test -> Push events`로 200 응답 확인 후 저장합니다.

### 6) 동작 확인
1. `test-gitlab.git`에 `index.html` 수정 후 push
2. Jenkins Job 자동 실행 확인
3. 배포 결과 확인: `http://localhost:8082`

### git lab 연동 시 plugin 확인
![](./1.png)

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
