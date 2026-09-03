from __future__ import annotations

import pytest
from app.services.ranking import BM25, combine_scores, cosine_similarity, tokenize


def test_cosine_similarity_bounds() -> None:
    assert cosine_similarity([1.0, 0.0, 1.0], [1.0, 0.0, 1.0]) == pytest.approx(1.0)
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_bm25_prefers_documents_with_query_terms() -> None:
    corpus = [tokenize("quarterly revenue and margins"), tokenize("office holiday schedule")]
    bm25 = BM25(corpus)
    terms = tokenize("revenue")
    assert bm25.score(terms, corpus[0]) > bm25.score(terms, corpus[1])


def test_combine_scores_weights_normalised_components() -> None:
    assert combine_scores(1.0, 0.0, alpha=0.5) == pytest.approx(0.5)
    assert combine_scores(0.0, 1.0, alpha=0.5) == pytest.approx(0.5)
    assert combine_scores(1.0, 1.0, alpha=0.5) == pytest.approx(1.0)
    assert 0.0 <= combine_scores(0.9, 0.1, alpha=0.7) <= 1.0
