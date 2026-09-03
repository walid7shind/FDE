from __future__ import annotations

import uuid

from fastapi import Depends, Header, HTTPException

from app.context import RequestContext, bind_context
from app.domain.models import User
from app.state import get_app_state


async def get_current_user(x_user_id: str | None = Header(default=None)) -> User:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="missing X-User-Id header")
    user = get_app_state().users.get(x_user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="unknown user")
    return user


async def request_context(user: User = Depends(get_current_user)) -> RequestContext:
    ctx = RequestContext(user=user, request_id=str(uuid.uuid4()))
    bind_context(ctx)
    return ctx
