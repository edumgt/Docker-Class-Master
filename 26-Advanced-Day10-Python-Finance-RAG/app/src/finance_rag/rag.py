from __future__ import annotations  # 타입 힌트 문자열 지연 평가 (Python 3.10 이전 호환성)

from dataclasses import dataclass  # 불변 데이터 클래스 생성 데코레이터
from pathlib import Path           # 파일 경로 조작을 위한 객체지향 API

from .ingest import load_chunks       # 같은 패키지의 ingest 모듈에서 청크 로더 임포트
from .retriever import TFIDFRetriever  # 같은 패키지의 retriever 모듈에서 TF-IDF 검색기 임포트


@dataclass(frozen=True)  # frozen=True: 반환 후 결과 수정 불가 (불변 응답 객체)
class RAGResult:
    """RAG(Retrieval-Augmented Generation) 질의응답 결과를 담는 불변 데이터 클래스."""
    answer: str          # TF-IDF 검색 결과를 기반으로 구성된 답변 텍스트
    citations: list[str] # 답변의 근거가 된 문서 참조 목록 (파일명 > 섹션 > 점수 형식)


class FinanceRAG:
    """금융공학 문서 기반 RAG 시스템. corpus를 로드하여 TF-IDF 검색으로 질의응답을 제공합니다."""

    def __init__(self, corpus_dir: Path) -> None:
        """corpus 디렉토리를 받아 문서를 로드하고 검색 인덱스를 구축합니다."""
        chunks = load_chunks(corpus_dir)
        # corpus_dir 내 마크다운 파일들을 읽어 Chunk 목록으로 변환

        self._retriever = TFIDFRetriever(chunks)
        # 로드된 Chunk 목록으로 TF-IDF 인덱스를 구축하여 검색기 초기화

    def ask(self, question: str, top_k: int = 3) -> RAGResult:
        """질문을 입력받아 관련 문서를 검색하고 RAGResult(답변 + 근거 문서)를 반환합니다."""
        results = self._retriever.search(question, top_k=top_k)
        # TF-IDF 검색기로 질문과 관련도 높은 상위 top_k 개의 청크 검색

        if not results:
            # 관련 청크가 하나도 없을 때 (질문과 매칭되는 단어가 없는 경우)
            return RAGResult(
                answer=(
                    "관련 근거를 찾지 못했습니다. 질의를 더 구체화하거나 "
                    "금리/파생상품/리스크/규제 키워드를 포함해 다시 질문해 주세요."
                ),
                citations=[],  # 근거 문서 없음
            )

        summary_points = [f"- {item.chunk.text}" for item in results]
        # 검색된 각 청크의 텍스트를 마크다운 목록 형식("- 내용")으로 변환

        citations = [
            f"{item.chunk.source} > {item.chunk.section} (score={item.score:.3f})"
            # 근거 문서 형식: "파일명 > 섹션 제목 (score=0.123)"
            # score:.3f: 점수를 소수점 3자리까지 표시
            for item in results
        ]

        answer = (
            "질문과 가장 관련 있는 금융공학 근거는 다음과 같습니다.\n"
            + "\n".join(summary_points)
            # 검색된 청크 내용들을 개행으로 연결하여 답변 본문 구성
            + "\n\n실무 적용 시에는 위 근거를 기준으로 모델 가정과 리스크 한계를 함께 검토하세요."
            # 실무 활용 시 주의사항 부가 안내
        )

        return RAGResult(answer=answer, citations=citations)
        # 완성된 답변과 근거 문서 목록을 RAGResult로 반환
