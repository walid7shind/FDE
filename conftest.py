from __future__ import annotations

from collections.abc import Iterator

import pytest
from app.services import search_service
from app.state import build_state, reset_state, set_app_state


@pytest.fixture(autouse=True)
def _reset_environment() -> Iterator[None]:
    search_service._RESULT_CACHE.clear()
    set_app_state(build_state())
    yield
    search_service._RESULT_CACHE.clear()
    reset_state()
