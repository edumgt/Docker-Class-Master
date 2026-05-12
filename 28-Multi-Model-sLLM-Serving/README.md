# 멀티 모델 & sLLM Docker 서빙 플레이그라운드

> Ollama를 중심으로 Gemma3, Llama 3, DeepSeek-R1 등 최신 오픈소스 sLLM을 Docker 환경에서 서빙하고 API·UI로 검증하는 실습입니다.

---

## 1) 실습 목표

- Ollama Docker 이미지로 CPU/GPU 서빙 환경을 구성한다.
- `gemma3`, `llama3`, `deepseek-r1` 모델을 Pull하고 추론 응답을 확인한다.
- Open WebUI로 브라우저 기반 멀티 모델 채팅 환경을 구성한다.
- REST API로 도메인 특화 프롬프트를 테스트한다.

---

## 2) 파일 구성

| 파일 | 설명 |
|---|---|
| `docker-compose.ollama.yml` | Ollama 단독 실행 (CPU 전용) |
| `docker-compose.ollama-gpu.yml` | Ollama 단독 실행 (NVIDIA GPU) |
| `docker-compose.stack.yml` | Ollama + Open WebUI 풀 스택 |

---

## 3) 빠른 시작

### A. CPU 전용 (로컬 노트북/서버)

```bash
cd 28-Multi-Model-sLLM-Serving

# Ollama 기동
docker compose -f docker-compose.ollama.yml up -d

# 상태 확인
docker compose -f docker-compose.ollama.yml ps

# 헬스체크
curl http://localhost:11434/
```

### B. NVIDIA GPU 가속

```bash
# NVIDIA Container Toolkit 사전 설치 필요
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

docker compose -f docker-compose.ollama-gpu.yml up -d
```

### C. Ollama + Open WebUI 풀 스택

```bash
docker compose -f docker-compose.stack.yml up -d

# UI 접속: http://localhost:3000
# (최초 접속 시 관리자 계정 생성)
```

---

## 4) 모델 Pull 및 서빙

Ollama가 기동된 상태에서 아래 명령으로 모델을 내려받습니다.

> [!NOTE]
> 모델 크기에 따라 수 GB의 디스크와 수 분의 다운로드 시간이 필요합니다.

### Gemma 3

```bash
# 2B (경량, CPU/GPU 공용)
docker exec -it ollama ollama pull gemma3:2b

# 12B (고성능, GPU 권장)
docker exec -it ollama ollama pull gemma3:12b
```

### Llama 3

```bash
# 8B
docker exec -it ollama ollama pull llama3:8b

# 70B (GPU 필수, VRAM 40GB+ 권장)
docker exec -it ollama ollama pull llama3:70b
```

### DeepSeek-R1

```bash
# 7B (추론 특화 경량 모델)
docker exec -it ollama ollama pull deepseek-r1:7b

# 14B
docker exec -it ollama ollama pull deepseek-r1:14b
```

### 기타 추천 모델

```bash
# Phi-4 (Microsoft, 14B)
docker exec -it ollama ollama pull phi4

# Mistral (7B)
docker exec -it ollama ollama pull mistral

# Qwen2.5 (7B, 다국어 강점)
docker exec -it ollama ollama pull qwen2.5:7b
```

### Pull된 모델 목록 확인

```bash
docker exec -it ollama ollama list
```

---

## 5) 추론 테스트

### CLI 대화

```bash
# 모델명은 pull한 태그 그대로 사용
docker exec -it ollama ollama run gemma3:2b
```

### REST API

```bash
# 단일 응답 (stream 비활성)
curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma3:2b",
    "prompt": "도커(Docker)와 가상머신(VM)의 차이를 3줄로 설명해줘.",
    "stream": false
  }' | python3 -m json.tool

# 채팅 형식 (멀티턴)
curl -s http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3:8b",
    "messages": [
      {"role": "user", "content": "DeepSeek-R1과 Llama 3의 성능 차이를 비교해줘."}
    ],
    "stream": false
  }' | python3 -m json.tool
```

### 모델 전환 (동일 API 엔드포인트)

```bash
# 모델명만 바꾸면 바로 전환 가능
for MODEL in gemma3:2b llama3:8b deepseek-r1:7b; do
  echo "=== $MODEL ==="
  curl -s http://localhost:11434/api/generate \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$MODEL\", \"prompt\": \"Hello! What model are you?\", \"stream\": false}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
done
```

---

## 6) 모델 삭제 및 정리

```bash
# 특정 모델 삭제
docker exec -it ollama ollama rm gemma3:12b

# 컨테이너 + 볼륨 전체 정리
docker compose -f docker-compose.ollama.yml down -v
```

---

## 7) 포트 요약

| 서비스 | 파일 | 주요 포트 | 용도 |
|---|---|---|---|
| Ollama (CPU) | `docker-compose.ollama.yml` | `11434` | REST API |
| Ollama (GPU) | `docker-compose.ollama-gpu.yml` | `11434` | REST API |
| Ollama | `docker-compose.stack.yml` | `11434` | REST API |
| Open WebUI | `docker-compose.stack.yml` | `3000` | 브라우저 UI |

---

## 8) 최소 자원 산정

| 모델 | 파라미터 | 최소 RAM | 권장 VRAM | 비고 |
|---|---:|---:|---:|---|
| `gemma3:2b` | 2B | 4 GB | — | CPU 서빙 가능 |
| `gemma3:12b` | 12B | 16 GB | 12 GB | GPU 권장 |
| `llama3:8b` | 8B | 8 GB | 8 GB | GPU 권장 |
| `llama3:70b` | 70B | 64 GB | 40 GB+ | GPU 필수 |
| `deepseek-r1:7b` | 7B | 8 GB | 8 GB | 추론 특화 |
| `deepseek-r1:14b` | 14B | 16 GB | 16 GB | GPU 권장 |

> [!IMPORTANT]
> CPU 전용 서빙 시 응답 속도가 GPU 대비 10~30배 느릴 수 있습니다.
> 실습 목적으로는 2B~8B 모델을 권장합니다.

---

## 9) GPU 설정 (NVIDIA Container Toolkit)

```bash
# Ubuntu/Debian 기준 설치
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# GPU 인식 확인
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

---

## 10) 체크리스트

- [ ] `docker-compose.ollama.yml`로 Ollama를 CPU 모드로 기동했다
- [ ] `ollama pull` 명령으로 최소 1개 모델(예: `gemma3:2b`)을 내려받았다
- [ ] REST API(`/api/generate`)로 추론 응답을 확인했다
- [ ] `docker-compose.stack.yml`로 Open WebUI를 기동하고 브라우저에서 접속했다
- [ ] 2개 이상의 모델을 전환하며 응답을 비교했다
- [ ] (선택) GPU 환경에서 `docker-compose.ollama-gpu.yml`로 가속 서빙을 확인했다

---

## 📺 관련 YouTube 영상

[🎬 YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=Ollama+Docker+Llama+Gemma+DeepSeek+sLLM)
