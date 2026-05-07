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
26-Advanced-Day10-Python-Finance-RAG/
├─ app/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ corpus/
│  │  ├─ derivatives_pricing.md
│  │  ├─ portfolio_risk.md
│  │  ├─ market_microstructure.md
│  │  └─ regulation_basics.md
│  └─ src/
│     ├─ run_lab.py
│     └─ finance_rag/
│        ├─ __init__.py
│        ├─ ingest.py
│        ├─ rag.py
│        └─ retriever.py
└─ docker-compose.yml
```

## 실행 방법

### 1) Docker Compose로 실행
```bash
cd 26-Advanced-Day10-Python-Finance-RAG
docker compose up --build
```

### 2) 로컬 Python 실행
```bash
cd 26-Advanced-Day10-Python-Finance-RAG/app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_lab.py
```

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
