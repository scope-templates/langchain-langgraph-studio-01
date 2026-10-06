"""Fuse keyword and dense candidates, then re-rank.

The current re-ranker is a local lexical overlap scorer. A hosted cross-encoder
or reranking service could replace `score` without touching the graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from app.retrieval.tokenize import content_terms


@dataclass(frozen=True)
class ScoredCandidate:
    chunk_id: str
    score: float


def reciprocal_rank_fusion(
    rankings: List[List[Tuple[str, float]]], k: int = 60
) -> List[Tuple[str, float]]:
    fused: Dict[str, float] = {}
    for ranking in rankings:
        for rank, (chunk_id, _score) in enumerate(ranking):
            fused[chunk_id] = fused.get(chunk_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(fused.items(), key=lambda x: x[1], reverse=True)


def lexical_overlap(query: str, text: str) -> float:
    q = set(content_terms(query))
    if not q:
        return 0.0
    d = content_terms(text)
    if not d:
        return 0.0
    hits = sum(1 for t in d if t in q)
    return hits / len(d)


def rerank(
    query: str,
    fused: List[Tuple[str, float]],
    chunk_text: Dict[str, str],
    limit: int,
) -> List[ScoredCandidate]:
    rescored: List[ScoredCandidate] = []
    for chunk_id, fusion_score in fused:
        text = chunk_text.get(chunk_id, "")
        overlap = lexical_overlap(query, text)
        combined = 0.65 * fusion_score + 0.35 * overlap
        rescored.append(ScoredCandidate(chunk_id=chunk_id, score=combined))
    rescored.sort(key=lambda c: c.score, reverse=True)
    return rescored[:limit]
