"""Sparse keyword candidate retrieval using a BM25-ish score."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from functools import lru_cache
from typing import Dict, List, Tuple

from app.knowledge_base.store import get_store
from app.retrieval.tokenize import content_terms

_K1 = 1.4
_B = 0.75


class KeywordIndex:
    def __init__(self) -> None:
        store = get_store()
        self._chunk_ids: List[str] = []
        self._term_freqs: List[Counter] = []
        self._lengths: List[int] = []
        df: Dict[str, int] = defaultdict(int)

        for chunk in store.chunks:
            terms = content_terms(chunk.text)
            tf = Counter(terms)
            self._chunk_ids.append(chunk.chunk_id)
            self._term_freqs.append(tf)
            self._lengths.append(len(terms))
            for term in tf:
                df[term] += 1

        n = max(len(self._chunk_ids), 1)
        self._idf = {
            term: math.log(1 + (n - freq + 0.5) / (freq + 0.5))
            for term, freq in df.items()
        }
        self._avg_len = (sum(self._lengths) / n) if self._lengths else 0.0

    def search(self, query: str, limit: int) -> List[Tuple[str, float]]:
        q_terms = content_terms(query)
        if not q_terms:
            return []
        scored: List[Tuple[str, float]] = []
        for idx, chunk_id in enumerate(self._chunk_ids):
            tf = self._term_freqs[idx]
            length = self._lengths[idx] or 1
            score = 0.0
            for term in q_terms:
                f = tf.get(term, 0)
                if not f:
                    continue
                idf = self._idf.get(term, 0.0)
                denom = f + _K1 * (
                    1 - _B + _B * length / (self._avg_len or 1)
                )
                score += idf * (f * (_K1 + 1)) / denom
            if score > 0:
                scored.append((chunk_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:limit]


@lru_cache(maxsize=1)
def get_keyword_index() -> KeywordIndex:
    return KeywordIndex()
