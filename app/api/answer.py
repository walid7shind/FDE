from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import request_context
from app.context import RequestContext
from app.domain.schemas import AnswerRequest, AnswerResponse
from app.state import get_app_state

router = APIRouter(tags=["answer"])


@router.post("/answer", response_model=AnswerResponse)
async def answer(
    payload: AnswerRequest, ctx: RequestContext = Depends(request_context)
) -> AnswerResponse:
    state = get_app_state()
    try:
        return await state.answer.answer(payload.query, payload.top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
