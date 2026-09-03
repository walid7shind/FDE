from __future__ import annotations

import pytest
from app.providers.base import ProviderError
from app.providers.embeddings import MockEmbeddingProvider
from app.providers.llm import MockLLMProvider
from app.services.ranking import cosine_similarity


async def test_embeddings_are_deterministic() -> None:
    provider = MockEmbeddingProvider()
    assert await provider.embed("hello world") == await provider.embed("hello world")


async def test_embeddings_reflect_token_overlap() -> None:
    provider = MockEmbeddingProvider()
    base = await provider.embed("quarterly revenue report")
    close = await provider.embed("quarterly revenue summary")
    far = await provider.embed("office holiday party schedule")
    assert cosine_similarity(base, close) > cosine_similarity(base, far)


async def test_llm_failure_raises_provider_error() -> None:
    with pytest.raises(ProviderError):
        await MockLLMProvider(fail=True).generate("q", ["ctx"])


async def test_embedding_failure_raises_provider_error() -> None:
    with pytest.raises(ProviderError):
        await MockEmbeddingProvider(fail=True).embed("q")
