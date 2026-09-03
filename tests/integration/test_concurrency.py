from __future__ import annotations

import asyncio

from tests.integration.util import build_client

ACME_DOCS = {"doc-acme-public", "doc-acme-tenant", "doc-acme-private-alice"}
GLOBEX_DOCS = {"doc-globex-public", "doc-globex-tenant", "doc-globex-private-dave"}


async def test_concurrent_searches_do_not_leak_across_tenants() -> None:
    async with build_client() as client:

        async def acme_call(i: int) -> None:
            resp = await client.post(
                "/search",
                json={"query": f"revenue margins {i}", "top_k": 5},
                headers={"X-User-Id": "u-alice"},
            )
            ids = {hit["document_id"] for hit in resp.json()["hits"]}
            assert ids <= ACME_DOCS, ("acme response leaked", ids)

        async def globex_call(i: int) -> None:
            resp = await client.post(
                "/search",
                json={"query": f"roadmap nautilus {i}", "top_k": 5},
                headers={"X-User-Id": "u-dave"},
            )
            ids = {hit["document_id"] for hit in resp.json()["hits"]}
            assert ids <= GLOBEX_DOCS, ("globex response leaked", ids)

        tasks = []
        for i in range(25):
            tasks.append(acme_call(i))
            tasks.append(globex_call(i))
        await asyncio.gather(*tasks)


async def test_concurrent_document_reads_keep_caller_identity() -> None:
    async with build_client() as client:

        async def read(user_id: str, document_id: str, expected_tenant: str) -> None:
            resp = await client.get(
                f"/documents/{document_id}", headers={"X-User-Id": user_id}
            )
            assert resp.status_code == 200, resp.text
            assert resp.json()["tenant_id"] == expected_tenant

        tasks = []
        for _ in range(25):
            tasks.append(read("u-alice", "doc-acme-private-alice", "acme"))
            tasks.append(read("u-dave", "doc-globex-private-dave", "globex"))
        await asyncio.gather(*tasks)
