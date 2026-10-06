def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["documents"] > 0
    assert body["chunks"] > 0


def test_retrieve_endpoint(client):
    resp = client.post(
        "/retrieve", json={"query": "drill battery care", "top_k": 4}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == len(body["results"])
    assert body["count"] <= 4
    assert all("url" in r and "score" in r for r in body["results"])


def test_retrieve_rejects_empty_query(client):
    resp = client.post("/retrieve", json={"query": ""})
    assert resp.status_code == 422


def test_retrieve_caps_top_k(client):
    resp = client.post(
        "/retrieve", json={"query": "tools", "top_k": 9999}
    )
    assert resp.status_code == 200
    assert resp.json()["top_k"] <= 25


def test_get_document_by_id(client):
    resp = client.get("/documents/care-ladders")
    assert resp.status_code == 200
    body = resp.json()
    assert body["doc_id"] == "care-ladders"
    assert "spreader" in body["body"]


def test_get_document_by_id_missing(client):
    resp = client.get("/documents/does-not-exist")
    assert resp.status_code == 404


def test_get_document_by_url(client):
    resp = client.get("/documents", params={"url": "/guides/canning-kits"})
    assert resp.status_code == 200
    assert resp.json()["doc_id"] == "care-canning"


def test_get_document_by_url_missing_param(client):
    resp = client.get("/documents")
    assert resp.status_code == 400
