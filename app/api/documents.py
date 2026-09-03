from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import request_context
from app.context import RequestContext
from app.domain.schemas import DocumentResponse
from app.state import get_app_state

router = APIRouter(tags=["documents"])


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str, ctx: RequestContext = Depends(request_context)
) -> DocumentResponse:
    state = get_app_state()
    try:
        document = state.documents.get(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="document not found")
        if not await state.policy.can_read_document(document):
            raise HTTPException(status_code=403, detail="not authorised to read this document")
        state.audit.record(ctx.user.tenant_id, ctx.user.user_id, "document.read", document_id)
        return DocumentResponse(**document.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
