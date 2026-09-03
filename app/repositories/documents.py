from __future__ import annotations

from app.domain.models import Document


class DocumentRepository:
    def __init__(self, documents: list[Document] | None = None) -> None:
        self._documents: dict[str, Document] = {}
        for document in documents or []:
            self._documents[document.document_id] = document

    def get(self, document_id: str) -> Document | None:
        return self._documents.get(document_id)

    def list_for_tenant(self, tenant_id: str) -> list[Document]:
        return [doc for doc in self._documents.values() if doc.tenant_id == tenant_id]

    def all(self) -> list[Document]:
        return list(self._documents.values())
