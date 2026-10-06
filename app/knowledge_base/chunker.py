"""Split documents into overlapping word-window chunks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List

from app.knowledge_base.documents import Document

_WORD_RE = re.compile(r"\S+")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    url: str
    tags: List[str]
    text: str
    position: int


def _words(text: str) -> List[str]:
    return _WORD_RE.findall(text)


def chunk_document(
    doc: Document, window: int, overlap: int
) -> List[Chunk]:
    if window <= 0:
        raise ValueError("window must be positive")
    if overlap >= window:
        raise ValueError("overlap must be smaller than window")

    words = _words(doc.body)
    if not words:
        return []

    step = window - overlap
    chunks: List[Chunk] = []
    position = 0
    start = 0
    while start < len(words):
        piece = words[start : start + window]
        text = " ".join(piece)
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}#{position}",
                doc_id=doc.doc_id,
                title=doc.title,
                url=doc.url,
                tags=list(doc.tags),
                text=text,
                position=position,
            )
        )
        if start + window >= len(words):
            break
        start += step
        position += 1
    return chunks


def chunk_all(
    docs: Iterable[Document], window: int, overlap: int
) -> List[Chunk]:
    out: List[Chunk] = []
    for doc in docs:
        out.extend(chunk_document(doc, window, overlap))
    return out
