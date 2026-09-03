from __future__ import annotations

import httpx


async def test_owner_reads_own_private_document(client: httpx.AsyncClient) -> None:
    resp = await client.get(
        "/documents/doc-acme-private-alice", headers={"X-User-Id": "u-alice"}
    )
    assert resp.status_code == 200
    assert resp.json()["document_id"] == "doc-acme-private-alice"


async def test_tenant_member_reads_tenant_document(client: httpx.AsyncClient) -> None:
    resp = await client.get("/documents/doc-acme-tenant", headers={"X-User-Id": "u-alice"})
    assert resp.status_code == 200


async def test_public_document_is_readable(client: httpx.AsyncClient) -> None:
    resp = await client.get("/documents/doc-acme-public", headers={"X-User-Id": "u-bob"})
    assert resp.status_code == 200


async def test_missing_auth_header_is_unauthorised(client: httpx.AsyncClient) -> None:
    resp = await client.get("/documents/doc-acme-public")
    assert resp.status_code == 401


async def test_unknown_document_returns_404(client: httpx.AsyncClient) -> None:
    resp = await client.get("/documents/no-such-doc", headers={"X-User-Id": "u-alice"})
    assert resp.status_code == 404


async def test_other_users_private_document_is_forbidden(client: httpx.AsyncClient) -> None:
    resp = await client.get(
        "/documents/doc-acme-private-alice", headers={"X-User-Id": "u-bob"}
    )
    assert resp.status_code == 403


async def test_cross_tenant_document_access_is_denied(client: httpx.AsyncClient) -> None:
    resp = await client.get("/documents/doc-globex-tenant", headers={"X-User-Id": "u-alice"})
    assert resp.status_code in (403, 404), resp.text
