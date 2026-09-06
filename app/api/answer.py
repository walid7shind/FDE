from __future__ import annotations
import asyncio

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import request_context
from app.context import RequestContext
from app.domain.schemas import AnswerRequest, AnswerResponse
from app.providers.base import ProviderError
from app.state import get_app_state

router = APIRouter(tags=["answer"])


@router.post("/answer", response_model=AnswerResponse)
async def answer(
    payload: AnswerRequest, ctx: RequestContext = Depends(request_context)
) -> AnswerResponse:
    state = get_app_state()
    try:
        return await asyncio.wait_for(state.answer.answer(payload.query,payload.top_k), timeout=2.0)
    except asyncio.TimeoutError:
        return AnswerResponse(answer="llm timed out",sources=[],degraded=True)
    except ProviderError:
        return AnswerResponse(answer="llm failed",sources=[],degraded=True)
