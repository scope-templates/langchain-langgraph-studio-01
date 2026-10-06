from app.retrieval.embeddings import cosine, embed
from app.retrieval.keyword_index import get_keyword_index
from app.retrieval.vector_index import get_vector_index


def test_embedding_is_normalized():
    v = embed("cordless drill battery charge")
    assert abs(float((v * v).sum()) - 1.0) < 1e-5


def test_related_text_more_similar_than_unrelated():
    q = embed("how do I care for the drill battery")
    related = embed("store the drill battery at half charge overnight")
    unrelated = embed("ladder spreader braces must be locked")
    assert cosine(q, related) > cosine(q, unrelated)


def test_keyword_index_finds_canning():
    hits = get_keyword_index().search("canning jars food safety", 5)
    assert hits
    assert any(cid.startswith("care-canning") for cid, _ in hits)


def test_vector_index_returns_ranked():
    hits = get_vector_index().search("sewing bobbin needle", 5)
    assert hits
    scores = [s for _, s in hits]
    assert scores == sorted(scores, reverse=True)
