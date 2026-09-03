from __future__ import annotations

import pytest
from app.domain.schemas import SearchRequest
from pydantic import ValidationError


def test_empty_query_is_rejected() -> None:
    with pytest.raises(ValidationError):
        SearchRequest(query="")


def test_whitespace_only_query_is_rejected() -> None:
    with pytest.raises(ValidationError):
        SearchRequest(query="   ")


def test_top_k_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        SearchRequest(query="hello", top_k=0)


def test_top_k_has_an_upper_bound() -> None:
    with pytest.raises(ValidationError):
        SearchRequest(query="hello", top_k=100_000)
