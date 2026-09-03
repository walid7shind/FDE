from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import request_context
from app.context import RequestContext
from app.domain.models import Role
from app.state import get_app_state

router = APIRouter(tags=["admin"])


@router.get("/admin/audit-logs")
async def audit_logs(
    ctx: RequestContext = Depends(request_context),
) -> dict[str, list[dict[str, Any]]]:
    if ctx.user.role != Role.admin:
        raise HTTPException(status_code=403, detail="admin role required")
    logs = get_app_state().audit.list_for_tenant(ctx.user.tenant_id)
    return {"logs": [entry.model_dump() for entry in logs]}
