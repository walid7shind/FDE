from __future__ import annotations

import asyncio

from app.context import current_context
from app.domain.models import Document, Visibility


class PolicyService:
    """Document-level access policy. Async to model a real ACL / policy-store lookup."""

    async def can_read_document(self, document: Document) -> bool:
        await asyncio.sleep(0)
        user = current_context().user
        if document.visibility == Visibility.public:
            return True
        if document.visibility == Visibility.tenant:
            return True
        return document.owner_id == user.user_id
