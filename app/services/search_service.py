from __future__ import annotations

from app.context import current_context
from app.domain.models import Document, User, Visibility
from app.domain.schemas import SearchHit
from app.providers.embeddings import MockEmbeddingProvider
from app.repositories.documents import DocumentRepository
from app.services.ranking import BM25, combine_scores, cosine_similarity, tokenize

_RESULT_CACHE: dict[str, list[SearchHit]] = {}


def _visible_to(user: User, document: Document) -> bool:
    if document.visibility in (Visibility.public, Visibility.tenant):
        return True
    return document.owner_id == user.user_id


def _snippet(content: str, length: int = 160) -> str:
    return content[:length]


class SearchService:
    def __init__(self, documents: DocumentRepository, embeddings: MockEmbeddingProvider) -> None:
        self._documents = documents
        self._embeddings = embeddings

    async def search(self, query: str, top_k: int = 5) -> tuple[list[SearchHit], bool]:
        cache_key = f"{query}|{top_k}"
        cached = _RESULT_CACHE.get(cache_key)
        if cached is not None:
            return cached, True

        query_vec = await self._embeddings.embed(query)
        query_terms = tokenize(query)

        ctx = current_context()
        documents = [
            doc
            for doc in self._documents.list_for_tenant(ctx.user.tenant_id)
            if _visible_to(ctx.user, doc)
        ]
        by_id = {doc.document_id: doc for doc in documents}
        corpus = [tokenize(doc.content) for doc in documents]

        bm25 = BM25(corpus)
        bm25_by_doc = {
            doc.document_id: bm25.score(query_terms, doc_terms)
            for doc, doc_terms in zip(documents, corpus, strict=True)
        }

        cosine_by_doc: dict[str, float] = {}
        for doc in documents:
            doc_vec = await self._embeddings.embed(doc.content)
            cosine_by_doc[doc.document_id] = cosine_similarity(query_vec, doc_vec)

        lexical = [doc_id for doc_id, score in bm25_by_doc.items() if score > 0.0]
        semantic = sorted(cosine_by_doc, key=lambda doc_id: cosine_by_doc[doc_id], reverse=True)
        semantic = semantic[:top_k]

        candidates = lexical + semantic
        hits = [
            SearchHit(
                document_id=doc_id,
                score=combine_scores(
                    bm25_by_doc.get(doc_id, 0.0), cosine_by_doc.get(doc_id, 0.0)
                ),
                snippet=_snippet(by_id[doc_id].content),
            )
            for doc_id in candidates
        ]
        hits.sort(key=lambda hit: hit.score)
        hits = hits[:top_k]

        _RESULT_CACHE[cache_key] = hits
        return hits, False
