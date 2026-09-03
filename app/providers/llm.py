from __future__ import annotations

import asyncio

from app.providers.base import ProviderError


class MockLLMProvider:
    """Deterministic extractive-style stub. Simulates network I/O with a cooperative yield."""

    def __init__(self, fail: bool = False, hang_seconds: float = 0.0) -> None:
        self.fail = fail
        self.hang_seconds = hang_seconds
        self.calls = 0

    async def generate(self, query: str, context: list[str]) -> str:
        self.calls += 1
        await asyncio.sleep(self.hang_seconds)
        if self.fail:
            raise ProviderError("llm provider unavailable")
        if not context:
            return f"I could not find supporting documents for: {query!r}."
        joined = " ".join(context)
        return f"Answer to {query!r} based on {len(context)} source(s): {joined[:280]}"
