# Thimbleby Tool Library — Retrieval API

The Thimbleby Community Tool Library lends out drills, ladders, canning kits and
sewing machines to residents. This service exposes the library's knowledge base
(member handbook, tool care guides, policy notes) over a small HTTP API so our
member-facing widgets and the front-desk terminal can pull *grounded* passages
instead of free text.

The API deliberately does **no** text generation. It only retrieves:

- `POST /retrieve` runs a multi-step pipeline (query expansion -> candidate
  gathering -> re-ranking) and returns ranked chunks with their source URLs.
- `GET /documents/{doc_id}` returns a whole document by its ID.
- `GET /documents?url=...` returns a whole document by its source URL.
- `GET /healthz` liveness probe.

## Running

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Retrieval pipeline

The pipeline is built with LangGraph as a small state machine. See
`app/pipeline/graph.py`. The re-ranking step is currently a local lexical scorer
in `app/retrieval/reranker.py`; optional LLM-based pruning of low-value chunks is
stubbed out behind the `prune` flag and not yet wired to anything.

## Layout

- `app/knowledge_base/` — the documents and the chunker.
- `app/retrieval/` — embeddings, candidate stores, re-ranker.
- `app/pipeline/` — the LangGraph retrieval graph and its typed state.
- `app/main.py` — FastAPI wiring.
- `tests/` — pipeline and HTTP tests.
