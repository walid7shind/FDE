from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


class BM25:
    def __init__(self, corpus: list[list[str]], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_count = len(corpus)
        self.avg_len = (sum(len(doc) for doc in corpus) / self.doc_count) if corpus else 0.0
        self.doc_freq: Counter[str] = Counter()
        for doc in corpus:
            for term in set(doc):
                self.doc_freq[term] += 1

    def _idf(self, term: str) -> float:
        n = self.doc_freq.get(term, 0)
        return math.log(1.0 + (self.doc_count - n + 0.5) / (n + 0.5))

    def score(self, query_terms: list[str], doc_terms: list[str]) -> float:
        if not doc_terms:
            return 0.0
        freqs = Counter(doc_terms)
        length = len(doc_terms)
        total = 0.0
        for term in query_terms:
            tf = freqs.get(term, 0)
            if tf == 0:
                continue
            numerator = tf * (self.k1 + 1.0)
            denominator = tf + self.k1 * (1.0 - self.b + self.b * length / (self.avg_len or 1.0))
            total += self._idf(term) * numerator / denominator
        return total


def combine_scores(bm25_score: float, cosine_score: float, alpha: float = 0.5) -> float:
    return bm25_score + cosine_score
