# 흐름-3: Docker Hub에서 LLM 이미지 내려받아 실행

> 이 실습에서는 로컬 LLM 서버(**Ollama**)와 벡터 데이터베이스(**Qdrant**)를 Docker Hub 이미지만으로 실행합니다.  
> 별도의 빌드 없이 `docker pull` → `docker run` → API 확인까지 진행합니다.

---

## 1. Docker 버전 확인 및 Docker Hub 로그인

```bash
docker version
docker login
```

---

## 2. Ollama — 로컬 LLM 서버

### 2-1. 이미지 Pull

```bash
docker pull ollama/ollama:latest
```

### 2-2. 컨테이너 실행

```bash
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama-data:/root/.ollama \
  ollama/ollama:latest
```

| 옵션 | 설명 |
|---|---|
| `-d` | 백그라운드(detach) 실행 |
| `-p 11434:11434` | 호스트 11434 → 컨테이너 11434 |
| `-v ollama-data:/root/.ollama` | 모델 파일 영구 저장 볼륨 |

### 2-3. 모델 다운로드 (컨테이너 내부)

```bash
docker exec -it ollama ollama pull llama3.2:1b
```

### 2-4. 추론 API 테스트

```bash
curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:1b","prompt":"hello","stream":false}'
```

### 2-5. 실행 중인 모델 목록 확인

```bash
curl -s http://localhost:11434/api/tags | python3 -m json.tool
```

---

## 3. Qdrant — 벡터 데이터베이스

### 3-1. 이미지 Pull

```bash
docker pull qdrant/qdrant:latest
```

### 3-2. 컨테이너 실행

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v qdrant-data:/qdrant/storage \
  qdrant/qdrant:latest
```

| 포트 | 용도 |
|---|---|
| `6333` | REST API / Web UI |
| `6334` | gRPC API |

### 3-3. 헬스체크

```bash
curl -s http://localhost:6333/healthz
# 응답: {"title":"qdrant - vector search engine","version":"..."}
```

### 3-4. Web UI 접속

브라우저에서 **http://localhost:6333/dashboard** 를 엽니다.

---

## 4. 이미지 · 컨테이너 상태 확인

```bash
# 이미지 목록
docker image ls

# 실행 중인 컨테이너
docker ps

# 전체 컨테이너(정지 포함)
docker ps -a
```

---

## 5. 컨테이너 중지 · 재시작 · 삭제

```bash
# 중지
docker stop ollama qdrant

# 재시작
docker start ollama qdrant

# 삭제 (중지 후)
docker stop ollama qdrant
docker rm ollama qdrant

# 이미지 삭제
docker rmi ollama/ollama:latest qdrant/qdrant:latest
```

---

## 6. Docker Compose로 한 번에 실행 (권장)

위 두 서비스를 동시에 실행하려면 `docker-compose.yml`을 사용합니다.

```bash
# 디렉터리 이동
cd 03-Pull-from-DockerHub-and-Run-Docker-Images

# 전체 스택 기동
docker compose up -d

# 로그 확인
docker compose logs -f

# 전체 스택 종료 및 정리
docker compose down
```

---

## 7. 실습 체크리스트

- [ ] `docker pull ollama/ollama:latest` 성공
- [ ] `docker pull qdrant/qdrant:latest` 성공
- [ ] Ollama `/api/generate` 응답 확인
- [ ] Qdrant `/healthz` 응답 확인
- [ ] `docker compose up -d` 로 두 서비스 동시 기동 확인
- [ ] `docker ps` 결과 캡처

---

## 📺 관련 YouTube 영상

[🎬 YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=Ollama+Qdrant+Docker+로컬+LLM+실습)
