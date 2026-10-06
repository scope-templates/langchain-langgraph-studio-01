"""Dense candidate retrieval over chunk embeddings."""

from __future__ import annotations

from functools import lru_cache
from typing import List, Tuple

import numpy as np

from app.knowledge_base.store import get_store
from app.retrieval.embeddings import embed, embed_many


class VectorIndex:
    def __init__(self) -> None:
        store = get_store()
        self._chunks = store.chunks
        self._matrix = embed_many([c.text for c in self._chunks])

    def search(self, query: str, limit: int) -> List[Tuple[str, float]]:
        if not self._chunks:
            return []
        q = embed(query)
        scores = self._matrix @ q
        order = np.argsort(-scores)[:limit]
        return [(self._chunks[i].chunk_id, float(scores[i])) for i in order]


@lru_cache(maxsize=1)
def get_vector_index() -> VectorIndex:
    return VectorIndex()
