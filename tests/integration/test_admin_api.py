from __future__ import annotations

import httpx


async def test_admin_can_list_audit_logs(client: httpx.AsyncClient) -> None:
    await client.get("/documents/doc-acme-public", headers={"X-User-Id": "u-alice"})
    resp = await client.get("/admin/audit-logs", headers={"X-User-Id": "u-carol"})
    assert resp.status_code == 200
    assert isinstance(resp.json()["logs"], list)


async def test_non_admin_cannot_list_audit_logs(client: httpx.AsyncClient) -> None:
    resp = await client.get("/admin/audit-logs", headers={"X-User-Id": "u-alice"})
    assert resp.status_code == 403


async def test_audit_logs_are_tenant_scoped(client: httpx.AsyncClient) -> None:
    await client.get("/documents/doc-acme-public", headers={"X-User-Id": "u-alice"})
    resp = await client.get("/admin/audit-logs", headers={"X-User-Id": "u-frank"})
    assert resp.status_code == 200
    tenants = {entry["tenant_id"] for entry in resp.json()["logs"]}
    assert tenants <= {"globex"}
