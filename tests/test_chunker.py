from app.knowledge_base.chunker import chunk_document
from app.knowledge_base.documents import Document


def _doc(body: str) -> Document:
    return Document(doc_id="d1", title="t", url="/d1", tags=[], body=body)


def test_short_document_single_chunk():
    chunks = chunk_document(_doc("one two three"), window=10, overlap=2)
    assert len(chunks) == 1
    assert chunks[0].text == "one two three"
    assert chunks[0].chunk_id == "d1#0"


def test_windows_overlap():
    body = " ".join(str(i) for i in range(20))
    chunks = chunk_document(_doc(body), window=8, overlap=3)
    assert len(chunks) >= 3
    first = chunks[0].text.split()
    second = chunks[1].text.split()
    assert first[-3:] == second[:3]


def test_empty_body_no_chunks():
    assert chunk_document(_doc("   "), window=5, overlap=1) == []


def test_overlap_must_be_smaller_than_window():
    import pytest

    with pytest.raises(ValueError):
        chunk_document(_doc("a b c"), window=4, overlap=4)
