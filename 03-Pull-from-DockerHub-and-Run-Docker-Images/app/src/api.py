"""FastAPI 기반 Finance RAG 웹 서버.

브라우저에서 금융공학 RAG 시스템을 테스트할 수 있는 REST API와
Vanilla JS + Tailwind CSS 프론트엔드를 제공합니다.
"""
from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from finance_rag import FinanceRAG

# ── 앱 초기화 ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Finance RAG API",
    description="금융공학 문서 기반 TF-IDF RAG 질의응답 API",
    version="1.0.0",
)

# FinanceRAG 인스턴스 (서버 기동 시 한 번만 초기화)
rag = FinanceRAG(corpus_dir=CORPUS_DIR)

# ── 스태틱 파일 마운트 ─────────────────────────────────────────────────────────
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── 스키마 ────────────────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    """질의 요청 스키마."""
    question: str
    top_k: int = 3


class AskResponse(BaseModel):
    """질의 응답 스키마."""
    answer: str
    citations: list[str]


# ── 엔드포인트 ────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root() -> HTMLResponse:
    """프론트엔드 SPA를 반환합니다."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<p>static/index.html not found</p>", status_code=404)


@app.get("/health")
async def health() -> dict[str, str]:
    """헬스체크 엔드포인트."""
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(body: AskRequest) -> AskResponse:
    """질문을 받아 금융공학 RAG 시스템에서 답변과 근거 문서를 반환합니다."""
    if not body.question.strip():
        return AskResponse(answer="질문을 입력해 주세요.", citations=[])

    top_k = max(1, min(body.top_k, 10))  # 1~10 범위 제한
    result = rag.ask(body.question.strip(), top_k=top_k)
    return AskResponse(answer=result.answer, citations=result.citations)


@app.get("/ask", response_model=AskResponse)
async def ask_get(
    q: Annotated[str, Query(description="질문 텍스트")],
    top_k: Annotated[int, Query(description="검색할 상위 청크 수", ge=1, le=10)] = 3,
) -> AskResponse:
    """GET 방식으로 질문을 받아 답변과 근거 문서를 반환합니다."""
    if not q.strip():
        return AskResponse(answer="질문을 입력해 주세요.", citations=[])

    result = rag.ask(q.strip(), top_k=top_k)
    return AskResponse(answer=result.answer, citations=result.citations)
