"""Request and response models for the HTTP API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.config import settings


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=settings.default_top_k, ge=1)
    prune: bool = Field(
        default=False,
        description="Request LLM pruning of low-value chunks (not yet active).",
    )


class RankedChunkOut(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    url: str
    text: str
    score: float


class RetrieveResponse(BaseModel):
    query: str
    top_k: int
    pruned: bool
    count: int
    results: List[RankedChunkOut]


class DocumentOut(BaseModel):
    doc_id: str
    title: str
    url: str
    tags: List[str]
    body: str


class ErrorOut(BaseModel):
    detail: str
    hint: Optional[str] = None
