from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import request_context
from app.context import RequestContext
from app.domain.schemas import SearchRequest, SearchResponse
from app.state import get_app_state

router = APIRouter(tags=["search"])


@router.post("/search", response_model=SearchResponse)
async def search(
    payload: SearchRequest, ctx: RequestContext = Depends(request_context)
) -> SearchResponse:
    state = get_app_state()
    try:
        hits, cached = await state.search.search(payload.query, payload.top_k)
        return SearchResponse(hits=hits, cached=cached)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
