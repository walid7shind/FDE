from __future__ import annotations

from dataclasses import dataclass

from app.domain.models import User


@dataclass
class RequestContext:
    user: User
    request_id: str


_active_context: RequestContext | None = None


def bind_context(ctx: RequestContext) -> None:
    global _active_context
    _active_context = ctx


def current_context() -> RequestContext:
    if _active_context is None:
        raise RuntimeError("request context has not been bound")
    return _active_context


def clear_context() -> None:
    global _active_context
    _active_context = None
