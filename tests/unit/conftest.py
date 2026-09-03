from __future__ import annotations

from collections.abc import Iterator

import pytest
from app.context import RequestContext, bind_context, clear_context
from app.domain.models import Role, User


@pytest.fixture
def acme_employee() -> User:
    return User(user_id="u-alice", tenant_id="acme", role=Role.employee)


@pytest.fixture
def bind_acme(acme_employee: User) -> Iterator[User]:
    bind_context(RequestContext(user=acme_employee, request_id="test-request"))
    yield acme_employee
    clear_context()
