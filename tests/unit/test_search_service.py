from __future__ import annotations

import pytest
from app.domain.models import User
from app.providers.embeddings import MockEmbeddingProvider
from app.repositories.documents import DocumentRepository
from app.repositories.seed import seed_documents
from app.services.search_service import SearchService


@pytest.fixture
def service() -> SearchService:
    return SearchService(DocumentRepository(seed_documents()), MockEmbeddingProvider())


async def test_search_returns_relevant_document_first(
    service: SearchService, bind_acme: User
) -> None:
    hits, cached = await service.search("office locations holidays", top_k=3)
    assert cached is False
    assert hits, "expected at least one hit"
    assert hits[0].document_id == "doc-acme-public"


async def test_results_sorted_by_descending_score(
    service: SearchService, bind_acme: User
) -> None:
    hits, _ = await service.search("revenue margins financials", top_k=5)
    scores = [hit.score for hit in hits]
    assert scores == sorted(scores, reverse=True)


async def test_results_contain_no_duplicate_documents(
    service: SearchService, bind_acme: User
) -> None:
    hits, _ = await service.search("revenue margins", top_k=10)
    ids = [hit.document_id for hit in hits]
    assert len(ids) == len(set(ids))
