from __future__ import annotations

import httpx

ACME = {"X-User-Id": "u-alice"}
GLOBEX = {"X-User-Id": "u-dave"}


async def test_search_returns_hits(client: httpx.AsyncClient) -> None:
    resp = await client.post("/search", json={"query": "revenue margins", "top_k": 5}, headers=ACME)
    assert resp.status_code == 200
    assert "hits" in resp.json()


async def test_search_orders_results_best_first(client: httpx.AsyncClient) -> None:
    resp = await client.post(
        "/search", json={"query": "office locations holidays", "top_k": 5}, headers=ACME
    )
    assert resp.status_code == 200
    hits = resp.json()["hits"]
    assert hits and hits[0]["document_id"] == "doc-acme-public"
    scores = [hit["score"] for hit in hits]
    assert scores == sorted(scores, reverse=True)


async def test_search_results_have_unique_document_ids(client: httpx.AsyncClient) -> None:
    resp = await client.post(
        "/search", json={"query": "revenue margins", "top_k": 10}, headers=ACME
    )
    ids = [hit["document_id"] for hit in resp.json()["hits"]]
    assert len(ids) == len(set(ids))


async def test_search_rejects_empty_query(client: httpx.AsyncClient) -> None:
    resp = await client.post("/search", json={"query": ""}, headers=ACME)
    assert resp.status_code == 422


async def test_search_rejects_excessive_top_k(client: httpx.AsyncClient) -> None:
    resp = await client.post("/search", json={"query": "revenue", "top_k": 5000}, headers=ACME)
    assert resp.status_code == 422


async def test_single_request_search_is_tenant_scoped(client: httpx.AsyncClient) -> None:
    resp = await client.post(
        "/search", json={"query": "roadmap nautilus acquisition", "top_k": 5}, headers=ACME
    )
    assert resp.status_code == 200
    ids = {hit["document_id"] for hit in resp.json()["hits"]}
    assert all(doc_id.startswith("doc-acme") for doc_id in ids)


async def test_search_cache_is_scoped_per_tenant(client: httpx.AsyncClient) -> None:
    body = {"query": "revenue margins roadmap", "top_k": 5}
    first = await client.post("/search", json=body, headers=ACME)
    assert first.status_code == 200
    second = await client.post("/search", json=body, headers=GLOBEX)
    assert second.status_code == 200
    ids = {hit["document_id"] for hit in second.json()["hits"]}
    assert all(doc_id.startswith("doc-globex") for doc_id in ids), ids
