"""The multi-step retrieval pipeline, built as a LangGraph state machine.

    expand -> gather_keyword -> gather_vector -> fuse_and_rerank -> (prune?)

The prune branch is reserved for an LLM-based chunk pruning step. It is not
implemented yet; the flag currently passes results through untouched.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, List

from langgraph.graph import END, START, StateGraph

from app.config import settings
from app.knowledge_base.store import get_store
from app.pipeline.expansion import expand_query
from app.pipeline.state import RankedChunk, RetrievalState
from app.retrieval.keyword_index import get_keyword_index
from app.retrieval.reranker import reciprocal_rank_fusion, rerank
from app.retrieval.vector_index import get_vector_index


def _node_expand(state: RetrievalState) -> RetrievalState:
    return {"expanded_queries": expand_query(state["query"])}


def _node_gather_keyword(state: RetrievalState) -> RetrievalState:
    index = get_keyword_index()
    pool = settings.candidate_pool
    merged: Dict[str, float] = {}
    for q in state["expanded_queries"]:
        for chunk_id, score in index.search(q, pool):
            merged[chunk_id] = max(merged.get(chunk_id, 0.0), score)
    ranked = sorted(merged.items(), key=lambda x: x[1], reverse=True)[:pool]
    return {"keyword_candidates": ranked}


def _node_gather_vector(state: RetrievalState) -> RetrievalState:
    index = get_vector_index()
    pool = settings.candidate_pool
    merged: Dict[str, float] = {}
    for q in state["expanded_queries"]:
        for chunk_id, score in index.search(q, pool):
            merged[chunk_id] = max(merged.get(chunk_id, 0.0), score)
    ranked = sorted(merged.items(), key=lambda x: x[1], reverse=True)[:pool]
    return {"vector_candidates": ranked}


def _node_fuse_and_rerank(state: RetrievalState) -> RetrievalState:
    store = get_store()
    chunk_map = {c.chunk_id: c for c in store.chunks}
    chunk_text = {cid: c.text for cid, c in chunk_map.items()}

    fused = reciprocal_rank_fusion(
        [state["keyword_candidates"], state["vector_candidates"]]
    )
    top_k = state.get("top_k", settings.default_top_k)
    scored = rerank(state["query"], fused, chunk_text, top_k)

    results: List[RankedChunk] = []
    for cand in scored:
        chunk = chunk_map.get(cand.chunk_id)
        if chunk is None:
            continue
        results.append(
            RankedChunk(
                chunk_id=chunk.chunk_id,
                doc_id=chunk.doc_id,
                title=chunk.title,
                url=store.absolute_url(chunk.url),
                text=chunk.text,
                score=round(cand.score, 6),
            )
        )
    return {"results": results}


def _node_prune(state: RetrievalState) -> RetrievalState:
    # TODO: send the ranked chunks to an LLM to drop ones that cannot help
    # answer the query, then return only the kept chunks. Not wired up yet.
    return {"results": state.get("results", [])}


def _route_prune(state: RetrievalState) -> str:
    return "prune" if state.get("prune") else "done"


@lru_cache(maxsize=1)
def build_pipeline():
    graph = StateGraph(RetrievalState)
    graph.add_node("expand", _node_expand)
    graph.add_node("gather_keyword", _node_gather_keyword)
    graph.add_node("gather_vector", _node_gather_vector)
    graph.add_node("fuse_and_rerank", _node_fuse_and_rerank)
    graph.add_node("prune", _node_prune)

    graph.add_edge(START, "expand")
    graph.add_edge("expand", "gather_keyword")
    graph.add_edge("gather_keyword", "gather_vector")
    graph.add_edge("gather_vector", "fuse_and_rerank")
    graph.add_conditional_edges(
        "fuse_and_rerank", _route_prune, {"prune": "prune", "done": END}
    )
    graph.add_edge("prune", END)
    return graph.compile()


def run_retrieval(
    query: str, top_k: int, prune: bool = False
) -> List[RankedChunk]:
    pipeline = build_pipeline()
    final_state = pipeline.invoke(
        {"query": query, "top_k": top_k, "prune": prune}
    )
    return final_state.get("results", [])
