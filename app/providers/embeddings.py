from __future__ import annotations

import asyncio
import hashlib
import math
import re

from app.config import settings
from app.providers.base import ProviderError

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _hashed_vector(text: str, dim: int) -> list[float]:
    vec = [0.0] * dim
    for token in _tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(value * value for value in vec)) or 1.0
    return [value / norm for value in vec]


class MockEmbeddingProvider:
    """Deterministic bag-of-tokens embedding. Simulates network I/O with a cooperative yield."""

    def __init__(
        self, dim: int | None = None, fail: bool = False, hang_seconds: float = 0.0
    ) -> None:
        self.dim = dim or settings.embedding_dim
        self.fail = fail
        self.hang_seconds = hang_seconds
        self.calls = 0

    async def embed(self, text: str) -> list[float]:
        self.calls += 1
        await asyncio.sleep(self.hang_seconds)
        if self.fail:
            raise ProviderError("embedding provider unavailable")
        return _hashed_vector(text, self.dim)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed(text) for text in texts]
