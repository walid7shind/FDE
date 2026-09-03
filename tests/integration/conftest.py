from __future__ import annotations

from collections.abc import AsyncIterator

import httpx
import pytest_asyncio

from tests.integration.util import build_client


@pytest_asyncio.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with build_client() as http_client:
        yield http_client
