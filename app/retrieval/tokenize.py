"""Shared tokenization and a small stopword list."""

from __future__ import annotations

import re
from typing import List

_TOKEN_RE = re.compile(r"[a-z0-9]+")

STOPWORDS = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "for",
        "from", "has", "have", "how", "i", "in", "is", "it", "its", "my",
        "of", "on", "or", "the", "to", "we", "what", "when", "where", "with",
        "you", "your",
    }
)


def tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text.lower())


def content_terms(text: str) -> List[str]:
    return [t for t in tokenize(text) if t not in STOPWORDS and len(t) > 1]
