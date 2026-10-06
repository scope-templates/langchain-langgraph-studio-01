from app.pipeline.expansion import expand_query
from app.pipeline.graph import run_retrieval


def test_expansion_includes_original():
    variants = expand_query("how do I renew a drill")
    assert variants[0] == "how do I renew a drill"
    assert len(variants) >= 2


def test_retrieval_returns_relevant_chunks():
    results = run_retrieval("what are the late fees for overdue tools", top_k=3)
    assert results
    assert len(results) <= 3
    doc_ids = {r["doc_id"] for r in results}
    assert "handbook-membership" in doc_ids or "policy-damage" in doc_ids


def test_results_sorted_by_score():
    results = run_retrieval("ladder safety on uneven ground", top_k=5)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_prune_flag_passes_through_for_now():
    plain = run_retrieval("parking near the library", top_k=3, prune=False)
    pruned = run_retrieval("parking near the library", top_k=3, prune=True)
    assert [r["chunk_id"] for r in plain] == [r["chunk_id"] for r in pruned]


def test_urls_are_absolute():
    results = run_retrieval("sewing machine threading", top_k=2)
    assert results
    assert all(r["url"].startswith("http") for r in results)
