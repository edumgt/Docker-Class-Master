from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from .ingest import Chunk

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9가-힣]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: Chunk
    score: float


class TFIDFRetriever:
    def __init__(self, chunks: Iterable[Chunk]) -> None:
        self._chunks = list(chunks)
        self._doc_term_counts: list[Counter[str]] = []
        self._idf: dict[str, float] = {}
        self._build_index()

    def _build_index(self) -> None:
        document_frequency: Counter[str] = Counter()
        for chunk in self._chunks:
            term_count = Counter(tokenize(chunk.text))
            self._doc_term_counts.append(term_count)
            document_frequency.update(term_count.keys())

        total_docs = max(len(self._chunks), 1)
        self._idf = {
            term: math.log((1 + total_docs) / (1 + df)) + 1.0
            for term, df in document_frequency.items()
        }

    def search(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        query_terms = tokenize(query)
        if not query_terms:
            return []

        query_count = Counter(query_terms)
        scored: list[RetrievedChunk] = []
        for idx, term_count in enumerate(self._doc_term_counts):
            score = 0.0
            for term, qtf in query_count.items():
                idf = self._idf.get(term, 0.0)
                dtf = term_count.get(term, 0)
                score += (qtf * idf) * (dtf * idf)
            if score > 0:
                scored.append(RetrievedChunk(chunk=self._chunks[idx], score=score))

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]
