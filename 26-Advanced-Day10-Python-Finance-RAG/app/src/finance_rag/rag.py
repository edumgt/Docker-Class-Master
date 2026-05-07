from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .ingest import load_chunks
from .retriever import TFIDFRetriever


@dataclass(frozen=True)
class RAGResult:
    answer: str
    citations: list[str]


class FinanceRAG:
    def __init__(self, corpus_dir: Path) -> None:
        chunks = load_chunks(corpus_dir)
        self._retriever = TFIDFRetriever(chunks)

    def ask(self, question: str, top_k: int = 3) -> RAGResult:
        results = self._retriever.search(question, top_k=top_k)
        if not results:
            return RAGResult(
                answer=(
                    "관련 근거를 찾지 못했습니다. 질의를 더 구체화하거나 "
                    "금리/파생상품/리스크/규제 키워드를 포함해 다시 질문해 주세요."
                ),
                citations=[],
            )

        summary_points = [f"- {item.chunk.text}" for item in results]
        citations = [
            f"{item.chunk.source} > {item.chunk.section} (score={item.score:.3f})"
            for item in results
        ]
        answer = (
            "질문과 가장 관련 있는 금융공학 근거는 다음과 같습니다.\n"
            + "\n".join(summary_points)
            + "\n\n실무 적용 시에는 위 근거를 기준으로 모델 가정과 리스크 한계를 함께 검토하세요."
        )
        return RAGResult(answer=answer, citations=citations)
