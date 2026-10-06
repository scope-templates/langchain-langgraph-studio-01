"""Typed state passed between pipeline nodes."""

from __future__ import annotations

from typing import List, Tuple, TypedDict


class RankedChunk(TypedDict):
    chunk_id: str
    doc_id: str
    title: str
    url: str
    text: str
    score: float


class RetrievalState(TypedDict, total=False):
    query: str
    top_k: int
    prune: bool
    expanded_queries: List[str]
    keyword_candidates: List[Tuple[str, float]]
    vector_candidates: List[Tuple[str, float]]
    results: List[RankedChunk]
