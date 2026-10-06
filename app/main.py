"""FastAPI application for the tool library retrieval service."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from app import __version__
from app.config import settings
from app.knowledge_base.store import get_store
from app.pipeline.graph import run_retrieval
from app.schemas import (
    DocumentOut,
    RankedChunkOut,
    RetrieveRequest,
    RetrieveResponse,
)

app = FastAPI(
    title="Thimbleby Tool Library Retrieval API",
    version=__version__,
    description=(
        "Retrieve ranked knowledge-base chunks or whole documents. "
        "No text generation is performed."
    ),
)


@app.get("/healthz")
def healthz() -> dict:
    store = get_store()
    return {
        "status": "ok",
        "version": __version__,
        "documents": len(store.documents),
        "chunks": len(store.chunks),
    }


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve(req: RetrieveRequest) -> RetrieveResponse:
    top_k = min(req.top_k, settings.max_top_k)
    results = run_retrieval(req.query, top_k=top_k, prune=req.prune)
    return RetrieveResponse(
        query=req.query,
        top_k=top_k,
        pruned=req.prune,
        count=len(results),
        results=[RankedChunkOut(**r) for r in results],
    )


@app.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: str) -> DocumentOut:
    store = get_store()
    doc = store.get_by_id(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"no document {doc_id!r}")
    return DocumentOut(
        doc_id=doc.doc_id,
        title=doc.title,
        url=store.absolute_url(doc.url),
        tags=list(doc.tags),
        body=doc.body,
    )


@app.get("/documents", response_model=DocumentOut)
def get_document_by_url(
    url: Optional[str] = Query(default=None, description="Source URL or path.")
) -> DocumentOut:
    if not url:
        raise HTTPException(status_code=400, detail="url query param required")
    store = get_store()
    doc = store.get_by_url(url)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"no document at {url!r}")
    return DocumentOut(
        doc_id=doc.doc_id,
        title=doc.title,
        url=store.absolute_url(doc.url),
        tags=list(doc.tags),
        body=doc.body,
    )
