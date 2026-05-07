from __future__ import annotations  # 타입 힌트 문자열 지연 평가 (Python 3.10 이전 호환성)

import math              # log 함수 등 수학 연산용
import re                # 정규표현식으로 토큰화
from collections import Counter  # 단어 빈도 집계에 최적화된 딕셔너리
from dataclasses import dataclass  # 불변 데이터 클래스 생성
from typing import Iterable        # 제네릭 이터러블 타입 힌트

from .ingest import Chunk  # 같은 패키지의 ingest 모듈에서 Chunk 데이터 클래스 임포트

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9가-힣]+")
# 영어(대소문자), 숫자, 한글 문자로 구성된 토큰만 추출하는 정규표현식
# 특수문자, 공백, 구두점은 토큰에서 제외


def tokenize(text: str) -> list[str]:
    """텍스트를 소문자 토큰 목록으로 변환합니다."""
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]
    # TOKEN_PATTERN.findall: 텍스트에서 유효한 토큰 패턴과 일치하는 모든 문자열 추출
    # .lower(): 대소문자 구분 없이 검색하기 위해 소문자로 통일


@dataclass(frozen=True)  # frozen=True: 불변 객체 (점수는 계산 후 변경 불필요)
class RetrievedChunk:
    """검색 결과로 반환되는 청크와 그 관련도 점수를 담는 불변 데이터 클래스."""
    chunk: Chunk   # 원본 Chunk 객체 (source, section, text 포함)
    score: float   # TF-IDF 기반 관련도 점수 (높을수록 질문과 관련성 높음)


class TFIDFRetriever:
    """TF-IDF(Term Frequency-Inverse Document Frequency) 알고리즘으로 관련 문서를 검색하는 검색기."""

    def __init__(self, chunks: Iterable[Chunk]) -> None:
        """청크 목록을 받아 TF-IDF 인덱스를 구축합니다."""
        self._chunks = list(chunks)              # Chunk 객체 목록 저장 (인덱스와 1:1 대응)
        self._doc_term_counts: list[Counter[str]] = []  # 각 청크의 단어 빈도(TF) 저장 리스트
        self._idf: dict[str, float] = {}         # 각 단어의 IDF 값 저장 딕셔너리
        self._build_index()                      # 인덱스 구축 메서드 호출

    def _build_index(self) -> None:
        """모든 청크를 순회하며 TF와 IDF를 계산하여 인덱스를 구축합니다."""
        document_frequency: Counter[str] = Counter()
        # 단어별 문서 빈도(DF) 집계: 특정 단어가 몇 개의 청크에 등장하는지 카운트

        for chunk in self._chunks:
            term_count = Counter(tokenize(chunk.text))
            # 각 청크의 텍스트를 토큰화하고 단어 빈도(TF) 계산
            self._doc_term_counts.append(term_count)       # 청크의 단어 빈도 저장
            document_frequency.update(term_count.keys())  # 각 단어의 DF 업데이트 (등장 청크 수 증가)

        total_docs = max(len(self._chunks), 1)
        # 전체 문서(청크) 수 (0으로 나누기 방지를 위해 최소값 1)

        self._idf = {
            term: math.log((1 + total_docs) / (1 + df)) + 1.0
            # IDF 공식: log((1 + N) / (1 + df)) + 1
            # N: 전체 문서 수, df: 해당 단어가 등장한 문서 수
            # +1 스무딩: 0으로 나누기 방지 및 미등장 단어에도 양수 IDF 부여
            for term, df in document_frequency.items()
        }  # 모든 단어에 대해 IDF 값 계산하여 딕셔너리로 저장

    def search(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        """질의 텍스트와 가장 관련도 높은 상위 top_k 개의 청크를 반환합니다."""
        query_terms = tokenize(query)  # 질의 텍스트를 토큰 목록으로 변환
        if not query_terms:
            return []  # 토큰이 없으면 빈 결과 반환 (빈 질의 처리)

        query_count = Counter(query_terms)  # 질의 내 각 단어 빈도(TF_q) 계산
        scored: list[RetrievedChunk] = []   # 점수가 계산된 청크들을 저장하는 리스트

        for idx, term_count in enumerate(self._doc_term_counts):
            # 각 청크에 대해 질의와의 유사도 점수 계산
            score = 0.0  # 이 청크의 누적 점수 초기화

            for term, qtf in query_count.items():
                # qtf: 질의에서 해당 단어의 등장 빈도
                idf = self._idf.get(term, 0.0)   # 해당 단어의 IDF 값 (없으면 0)
                dtf = term_count.get(term, 0)    # 청크에서 해당 단어의 등장 빈도 (없으면 0)
                score += (qtf * idf) * (dtf * idf)
                # 점수 공식: (질의TF × IDF) × (문서TF × IDF)
                # 질의와 문서 양쪽에서 자주 등장할수록, IDF가 높을수록(희귀 단어일수록) 점수 높음

            if score > 0:
                scored.append(RetrievedChunk(chunk=self._chunks[idx], score=score))
                # 점수가 0보다 큰 청크만 결과에 포함 (완전히 무관한 청크 제외)

        scored.sort(key=lambda item: item.score, reverse=True)
        # 점수 내림차순으로 정렬 (가장 관련성 높은 청크가 앞으로)

        return scored[:top_k]  # 상위 top_k 개의 청크만 반환
