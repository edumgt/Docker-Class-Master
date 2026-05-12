# Vector DB Docker Playground

> 경량 오픈소스 Vector DB를 Docker Compose로 빠르게 실행/비교하는 실습입니다.

---

## 1) 실습 목표
- Vector DB의 공통 개념(임베딩, ANN, 유사도, 필터링)을 실습 관점에서 이해한다.
- Qdrant, Chroma, Weaviate, pgvector를 Docker로 단독 기동한다.
- 서비스별 기본 헬스체크/접속 포인트를 확인한다.

---

## 2) 빠른 시작
```bash
cd 27-Vector-DB-Docker-Playground

# 예시) Qdrant 기동
docker compose -f docker-compose.qdrant.yml up -d

# 상태 확인
docker compose -f docker-compose.qdrant.yml ps

# 종료/정리
docker compose -f docker-compose.qdrant.yml down
```

---

## 3) 예제 목록

### A. Qdrant
```bash
docker compose -f docker-compose.qdrant.yml up -d
curl -s http://localhost:6333/healthz
# Dashboard: http://localhost:6333/dashboard
```

### B. Chroma
```bash
docker compose -f docker-compose.chroma.yml up -d
curl -s http://localhost:8000/api/v1/heartbeat
```

### C. Weaviate
```bash
docker compose -f docker-compose.weaviate.yml up -d
curl -s http://localhost:8080/v1/.well-known/ready
```

### D. pgvector (PostgreSQL)
```bash
# 비밀번호를 환경변수로 지정(권장)
export POSTGRES_PASSWORD='replace-with-strong-password'

docker compose -f docker-compose.pgvector.yml up -d

# 확장 확인
docker exec -it pgvector psql -U vector_admin -d vectordb -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

## 4) 포트 요약
| 서비스 | 파일 | 주요 포트 |
|---|---|---|
| Qdrant | `docker-compose.qdrant.yml` | `6333`, `6334` |
| Chroma | `docker-compose.chroma.yml` | `8000` |
| Weaviate | `docker-compose.weaviate.yml` | `8080`, `50051` |
| pgvector | `docker-compose.pgvector.yml` | `5432` |

---

## 5) 체크리스트
- [ ] Qdrant/Chroma/Weaviate/pgvector 중 최소 2개 이상 기동했다
- [ ] 각 서비스 헬스체크 응답을 확인했다
- [ ] 볼륨 기반 데이터 영속성(재시작 후 유지)을 확인했다

---

## 📺 관련 YouTube 영상

[🎬 YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=Vector+DB+Docker+Qdrant+Chroma+Weaviate+pgvector)
