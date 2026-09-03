from __future__ import annotations

from typing import Any

from app.domain.models import Document, Role, User, Visibility
from app.services.policy import PolicyService

ALICE = User(user_id="u-alice", tenant_id="acme", role=Role.employee)
BOB = User(user_id="u-bob", tenant_id="acme", role=Role.manager)


def _doc(**overrides: Any) -> Document:
    base: dict[str, Any] = {
        "document_id": "doc-1",
        "tenant_id": "acme",
        "owner_id": "u-bob",
        "visibility": Visibility.tenant,
        "content": "internal",
        "metadata": {},
    }
    base.update(overrides)
    return Document(**base)


async def test_public_document_is_readable(bind_acme: User) -> None:
    assert await PolicyService().can_read_document(_doc(visibility=Visibility.public))


async def test_tenant_document_is_readable_by_tenant_member(bind_acme: User) -> None:
    assert await PolicyService().can_read_document(
        _doc(visibility=Visibility.tenant, tenant_id="acme")
    )


async def test_private_document_readable_by_owner(bind_acme: User) -> None:
    assert await PolicyService().can_read_document(
        _doc(visibility=Visibility.private, owner_id="u-alice")
    )


async def test_private_document_not_readable_by_other_user(bind_acme: User) -> None:
    assert not await PolicyService().can_read_document(
        _doc(visibility=Visibility.private, owner_id="u-bob")
    )
