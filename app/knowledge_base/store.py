"""In-memory document and chunk store."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, List, Optional

from app.config import settings
from app.knowledge_base.chunker import Chunk, chunk_all
from app.knowledge_base.documents import RAW_DOCUMENTS, Document


def _normalize_url(url: str) -> str:
    url = url.strip()
    for prefix in (settings.base_url,):
        if url.startswith(prefix):
            url = url[len(prefix) :]
    if not url.startswith("/"):
        url = "/" + url
    return url.rstrip("/") or "/"


class DocumentStore:
    def __init__(self, documents: List[Document]):
        self._by_id: Dict[str, Document] = {d.doc_id: d for d in documents}
        self._by_url: Dict[str, Document] = {
            _normalize_url(d.url): d for d in documents
        }
        self._chunks: List[Chunk] = chunk_all(
            documents, settings.chunk_tokens, settings.chunk_overlap
        )

    @property
    def documents(self) -> List[Document]:
        return list(self._by_id.values())

    @property
    def chunks(self) -> List[Chunk]:
        return list(self._chunks)

    def get_by_id(self, doc_id: str) -> Optional[Document]:
        return self._by_id.get(doc_id)

    def get_by_url(self, url: str) -> Optional[Document]:
        return self._by_url.get(_normalize_url(url))

    def absolute_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return settings.base_url.rstrip("/") + url


@lru_cache(maxsize=1)
def get_store() -> DocumentStore:
    return DocumentStore(RAW_DOCUMENTS)
