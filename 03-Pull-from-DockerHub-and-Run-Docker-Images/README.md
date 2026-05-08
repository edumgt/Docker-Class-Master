# 흐름-1: Docker Hub에서 이미지 내려받아 실행

## 1. Docker 버전 확인 및 Docker Hub 로그인
```bash
docker version
docker login
```

## 2. Docker Hub에서 이미지 Pull
```bash
docker pull stacksimplify/dockerintro-springboot-helloworld-rest-api:1.0.0-RELEASE
```

## 3. 이미지 실행 및 애플리케이션 접속
- Docker Hub에서 이미지 이름을 복사해 실행합니다.
```bash
docker run --name app1 -p 80:8080 -d stacksimplify/dockerintro-springboot-helloworld-rest-api:1.0.0-RELEASE
```

### 이미지 목록 확인
```bash
docker image ls
```

### 브라우저 접속
- http://localhost/hello

![alt text](image.png)
![alt text](image-1.png)

## 보강: Ollama 로컬 LLM 컨테이너 실행 예시

### 1) Ollama 이미지 Pull
```bash
docker pull ollama/ollama:latest
```

### 2) Ollama 서버 실행 (모델 저장 볼륨 포함)
```bash
docker run -d --name ollama -p 11434:11434 -v ollama-data:/root/.ollama ollama/ollama:latest
```

### 3) 모델 다운로드
```bash
docker exec -it ollama ollama pull llama3.2:1b
```

### 4) 추론 API 호출
```bash
curl -s http://localhost:11434/api/generate \
  -d '{"model":"llama3.2:1b","prompt":"hello","stream":false}'
```

### 5) 정리
```bash
docker stop ollama
docker rm ollama
```

## 참고: Apple Silicon(Mac) 환경
1. Apple Silicon용 Docker Desktop을 설치합니다.
   - https://docs.docker.com/desktop/mac/install/
2. 아래 명령으로 Nginx 컨테이너를 실행합니다.

```bash
docker run --name kube1 -p 80:80 --platform linux/amd64 -d stacksimplify/kubenginx:1.0.0
```

- http://localhost

### 예시 출력
```text
kalyanreddy@Kalyans-Mac-mini-2 ~ % docker run --name kube1 -p 80:80 --platform linux/amd64 -d  stacksimplify/kubenginx:1.0.0
370f238d97556813a4978572d24983d6aaf80d4300828a57f27cda3d3d8f0fec
kalyanreddy@Kalyans-Mac-mini-2 ~ % curl http://localhost
<!DOCTYPE html>
<html>
   <body style="background-color:lightgoldenrodyellow;">
      <h1>Welcome to Stack Simplify</h1>
      <p>Kubernetes Fundamentals Demo</p>
      <p>Application Version: V1</p>
   </body>
</html>%
kalyanreddy@Kalyans-Mac-mini-2 ~ %
```

## 4. 실행 중인 컨테이너 목록 확인
```bash
docker ps
docker ps -a
docker ps -a -q
```

### Docker Desktop 목록 확인(동일 내용)
![alt text](image-2.png)

## 5. 컨테이너 터미널 접속
```bash
docker exec -it <container-name> /bin/sh
```

![alt text](image-3.png)

### 예시
```text
PS C:\edumgt-java-education\docker-fundamentals> docker exec -it app1 /bin/sh
/ # ls -al
total 18840
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 .
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 ..
-rwxr-xr-x    1 root     root             0 Jun 29 01:31 .dockerenv
-rw-r--r--    1 root     root      19225249 Nov 23  2019 app.jar
drwxr-xr-x    2 root     root          4096 May  9  2019 bin
drwxr-xr-x    5 root     root           340 Jun 29 01:31 dev
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 etc
drwxr-xr-x    2 root     root          4096 May  9  2019 home
drwxr-xr-x    1 root     root          4096 May 11  2019 lib
drwxr-xr-x    5 root     root          4096 May  9  2019 media
drwxr-xr-x    2 root     root          4096 May  9  2019 mnt
drwxr-xr-x    2 root     root          4096 May  9  2019 opt
dr-xr-xr-x  322 root     root             0 Jun 29 01:31 proc
drwx------    1 root     root          4096 Jun 29 01:36 root
drwxr-xr-x    2 root     root          4096 May  9  2019 run
drwxr-xr-x    2 root     root          4096 May  9  2019 sbin
drwxr-xr-x    2 root     root          4096 May  9  2019 srv
dr-xr-xr-x   13 root     root             0 Jun 29 01:31 sys
drwxrwxrwt    5 root     root          4096 Jun 29 01:31 tmp
drwxr-xr-x    1 root     root          4096 May 11  2019 usr
drwxr-xr-x    1 root     root          4096 May  9  2019 var
/ # exit
PS C:\edumgt-java-education\docker-fundamentals> docker exec -it 300039d4d0f39ce638d9678765d09ab92705c42544b6920f30f5e2c14890cfca /bin/sh
/ # ls -al
total 18840
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 .
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 ..
-rwxr-xr-x    1 root     root             0 Jun 29 01:31 .dockerenv
-rw-r--r--    1 root     root      19225249 Nov 23  2019 app.jar
drwxr-xr-x    2 root     root          4096 May  9  2019 bin
drwxr-xr-x    5 root     root           340 Jun 29 01:31 dev
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 etc
drwxr-xr-x    2 root     root          4096 May  9  2019 home
drwxr-xr-x    1 root     root          4096 May 11  2019 lib
drwxr-xr-x    5 root     root          4096 May  9  2019 media
drwxr-xr-x    2 root     root          4096 May  9  2019 mnt
drwxr-xr-x    2 root     root          4096 May  9  2019 opt
dr-xr-xr-x  319 root     root             0 Jun 29 01:31 proc
drwx------    1 root     root          4096 Jun 29 01:36 root
drwxr-xr-x    2 root     root          4096 Jun 29 01:31 run
drwxr-xr-x    2 root     root          4096 Jun 29 01:31 sbin
drwxr-xr-x    2 root     root          4096 May  9  2019 srv
dr-xr-xr-x   13 root     root             0 Jun 29 01:31 sys
drwxrwxrwt    5 root     root          4096 Jun 29 01:31 tmp
drwxr-xr-x    1 root     root          4096 May 11  2019 usr
drwxr-xr-x    1 root     root          4096 May  9  2019 var
/ # exit
PS C:\edumgt-java-education\docker-fundamentals>
```

## 6. 컨테이너 중지 및 시작
```bash
docker stop <container-name>
docker start <container-name>
```

## 7. 컨테이너 삭제
```bash
docker stop <container-name>
docker rm <container-name>
```

## 8. 이미지 삭제
```bash
docker images
docker rmi <image-id>
```

## Docker Desktop에서 상태 확인
![alt text](image-4.png)
- `:` 클릭 → 상세 뷰 클릭

![alt text](image-5.png)

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

---

## 📺 관련 YouTube 영상

[🎬 YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=Docker+Hub+이미지+pull+run)

---

# Day 10 — Python + 금융공학 RAG Lab

## 목표
- 금융공학 도메인 문서를 로컬에서 수집/청크/검색하는 RAG 파이프라인을 구현한다.
- Python 표준 라이브러리 기반으로 임베딩 대체 검색(TF-IDF 유사 스코어)을 실습한다.
- Docker Compose로 실습 환경을 고정하고 재현 가능한 Lab 흐름을 완성한다.

## 커리큘럼 구성

| 모듈 | 주제 | 실습 산출물 |
|---|---|---|
| Module 1 | 금융공학 RAG 개요(지식베이스/리트리버/응답생성) | 아키텍처 스케치 |
| Module 2 | 문서 수집/청킹 전략(헤더 기반 + 문단 분할) | 청크 JSON 확인 |
| Module 3 | 검색 스코어링(TF-IDF 유사)과 Top-K 근거 선택 | 질의별 검색 결과 |
| Module 4 | 근거 포함 답변 생성(출처 표기) | 답변 + citations |
| Module 5 | 평가/개선(질의셋, chunk 크기, stopword, k값 튜닝) | 개선 리포트 |

## 권장 진행
- 30m: 도메인/시나리오 설명
- 60m: 인덱싱 파이프라인 실행
- 90m: 질의 실습(금리/파생상품/리스크/규제)
- 60m: 검색 품질 개선 과제
- 30m: 리뷰 및 회고

## 폴더 구조
```text
03-Pull-from-DockerHub-and-Run-Docker-Images/
├─ app/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ corpus/
│  │  ├─ derivatives_pricing.md
│  │  ├─ portfolio_risk.md
│  │  ├─ market_microstructure.md
│  │  └─ regulation_basics.md
│  ├─ static/
│  │  └─ index.html          ← Vanilla JS + Tailwind CSS 프론트엔드
│  └─ src/
│     ├─ api.py               ← FastAPI 백엔드
│     ├─ run_lab.py           ← CLI 실습 진입점 (레거시)
│     └─ finance_rag/
│        ├─ __init__.py
│        ├─ ingest.py
│        ├─ rag.py
│        └─ retriever.py
└─ docker-compose.yml
```

## 실행 방법

### 1) Docker Compose로 실행 (권장)
```bash
cd 03-Pull-from-DockerHub-and-Run-Docker-Images
docker compose up --build
```
서버가 기동되면 브라우저에서 **http://localhost:8000** 을 열어 웹 UI를 사용합니다.

### 2) 로컬 Python 실행
```bash
cd 03-Pull-from-DockerHub-and-Run-Docker-Images/app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000 --app-dir src
```
브라우저에서 **http://localhost:8000** 접속.

### API 엔드포인트
| 메서드 | 경로 | 설명 |
|---|---|---|
| `GET` | `/` | 웹 UI (프론트엔드 SPA) |
| `GET` | `/health` | 헬스체크 |
| `POST` | `/ask` | JSON 바디로 질문 (`question`, `top_k`) |
| `GET` | `/ask?q=질문` | 쿼리 파라미터로 질문 |
| `GET` | `/docs` | Swagger UI (자동 생성) |
| `GET` | `/redoc` | ReDoc API 문서 |

## 예시 질의
- `듀레이션과 금리 민감도 관계를 설명해줘`
- `VaR와 Expected Shortfall의 차이는 무엇인가?`
- `시장 충격 시 유동성 리스크를 줄이기 위한 주문 전략은?`
- `파생상품 데스크에서 모델 리스크를 줄이는 운영 통제는?`

## 체크리스트
- [ ] 문서 인덱싱 결과(`chunks`)를 확인했다
- [ ] 최소 5개 질의를 실행하고 근거 문서를 검토했다
- [ ] 오답 1개를 분석하고 chunk/k/질의문 개선안을 기록했다
- [ ] 팀 기준 평가표(정확성/근거성/재현성)를 작성했다

---

## 📺 관련 YouTube 영상

[🎬 YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=Python+금융공학+RAG+LLM+실습)
