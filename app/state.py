from __future__ import annotations

from dataclasses import dataclass

from app.domain.models import Document, User
from app.providers.embeddings import MockEmbeddingProvider
from app.providers.llm import MockLLMProvider
from app.repositories.audit import AuditRepository
from app.repositories.documents import DocumentRepository
from app.repositories.seed import seed_documents, seed_users
from app.repositories.users import UserRepository
from app.services.answer_service import AnswerService
from app.services.policy import PolicyService
from app.services.search_service import SearchService


@dataclass
class AppState:
    users: UserRepository
    documents: DocumentRepository
    audit: AuditRepository
    embeddings: MockEmbeddingProvider
    llm: MockLLMProvider
    policy: PolicyService
    search: SearchService
    answer: AnswerService


def build_state(
    users: list[User] | None = None,
    documents: list[Document] | None = None,
    embeddings: MockEmbeddingProvider | None = None,
    llm: MockLLMProvider | None = None,
) -> AppState:
    users_repo = UserRepository(users if users is not None else seed_users())
    documents_repo = DocumentRepository(
        documents if documents is not None else seed_documents()
    )
    audit_repo = AuditRepository()
    embedding_provider = embeddings or MockEmbeddingProvider()
    llm_provider = llm or MockLLMProvider()
    search_service = SearchService(documents_repo, embedding_provider)
    answer_service = AnswerService(search_service, llm_provider)
    return AppState(
        users=users_repo,
        documents=documents_repo,
        audit=audit_repo,
        embeddings=embedding_provider,
        llm=llm_provider,
        policy=PolicyService(),
        search=search_service,
        answer=answer_service,
    )


_state: AppState | None = None


def set_app_state(state: AppState) -> None:
    global _state
    _state = state


def get_app_state() -> AppState:
    if _state is None:
        raise RuntimeError("application state has not been initialised")
    return _state


def reset_state() -> None:
    global _state
    _state = None
