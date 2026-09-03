from __future__ import annotations

from app.domain.schemas import AnswerResponse
from app.providers.llm import MockLLMProvider
from app.services.search_service import SearchService


class AnswerService:
    def __init__(self, search: SearchService, llm: MockLLMProvider) -> None:
        self._search = search
        self._llm = llm

    async def answer(self, query: str, top_k: int = 5) -> AnswerResponse:
        hits, _cached = await self._search.search(query, top_k)
        context = [hit.snippet for hit in hits]
        text = await self._llm.generate(query, context)
        return AnswerResponse(answer=text, sources=hits, degraded=False)
