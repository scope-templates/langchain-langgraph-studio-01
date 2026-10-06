"""A small deterministic hashing embedder.

This stands in for a hosted embedding model. It is intentionally simple and
local: a hashing bag-of-words projected into a fixed-dimension vector, then
L2-normalized. Good enough for ranking within this knowledge base and has no
external dependency.
"""

from __future__ import annotations

import hashlib
from typing import List

import numpy as np

from app.retrieval.tokenize import content_terms

DIM = 256


def _bucket(term: str) -> int:
    digest = hashlib.blake2b(term.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") % DIM


def embed(text: str) -> np.ndarray:
    vec = np.zeros(DIM, dtype=np.float32)
    terms = content_terms(text)
    for term in terms:
        vec[_bucket(term)] += 1.0
    norm = float(np.linalg.norm(vec))
    if norm > 0:
        vec /= norm
    return vec


def embed_many(texts: List[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, DIM), dtype=np.float32)
    return np.vstack([embed(t) for t in texts])


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))
