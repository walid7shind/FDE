from __future__ import annotations

import time

import httpx
import pytest
from app.providers.llm import MockLLMProvider
from app.state import build_state

from tests.integration.util import build_client

ACME = {"X-User-Id": "u-alice"}


async def test_answer_returns_text_and_sources(client: httpx.AsyncClient) -> None:
    resp = await client.post(
        "/answer", json={"query": "what are the office holidays", "top_k": 3}, headers=ACME
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["answer"]
    assert isinstance(body["sources"], list)


async def test_answer_degrades_when_llm_fails() -> None:
    state = build_state(llm=MockLLMProvider(fail=True))
    async with build_client(state) as client:
        resp = await client.post(
            "/answer", json={"query": "summarise revenue", "top_k": 3}, headers=ACME
        )
    assert resp.status_code == 200, resp.text
    assert resp.json()["degraded"] is True


@pytest.mark.slow
async def test_answer_times_out_on_slow_llm() -> None:
    state = build_state(llm=MockLLMProvider(hang_seconds=3.0))
    async with build_client(state) as client:
        started = time.perf_counter()
        resp = await client.post(
            "/answer", json={"query": "summarise revenue", "top_k": 3}, headers=ACME
        )
        elapsed = time.perf_counter() - started
    assert resp.status_code == 200, resp.text
    assert resp.json()["degraded"] is True
    assert elapsed < 2.5
