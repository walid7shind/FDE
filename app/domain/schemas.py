from __future__ import annotations

from pydantic import BaseModel

from app.config import settings


class DocumentResponse(BaseModel):
    document_id: str
    tenant_id: str
    owner_id: str
    visibility: str
    content: str
    metadata: dict[str, str]


class SearchRequest(BaseModel):
    query: str
    top_k: int = settings.default_top_k
    tenant_id: str | None = None


class SearchHit(BaseModel):
    document_id: str
    score: float
    snippet: str


class SearchResponse(BaseModel):
    hits: list[SearchHit]
    cached: bool = False


class AnswerRequest(BaseModel):
    query: str
    top_k: int = settings.default_top_k
    tenant_id: str | None = None


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SearchHit]
    degraded: bool = False
