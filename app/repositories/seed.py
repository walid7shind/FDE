from __future__ import annotations

from app.domain.models import Document, Role, User, Visibility


def seed_users() -> list[User]:
    return [
        User(user_id="u-alice", tenant_id="acme", role=Role.employee),
        User(user_id="u-bob", tenant_id="acme", role=Role.manager),
        User(user_id="u-carol", tenant_id="acme", role=Role.admin),
        User(user_id="u-dave", tenant_id="globex", role=Role.employee),
        User(user_id="u-erin", tenant_id="globex", role=Role.manager),
        User(user_id="u-frank", tenant_id="globex", role=Role.admin),
    ]


def seed_documents() -> list[Document]:
    return [
        Document(
            document_id="doc-acme-public",
            tenant_id="acme",
            owner_id="u-bob",
            visibility=Visibility.public,
            content="ACME employee handbook: office locations, holidays and travel policy.",
            metadata={"title": "ACME Handbook", "category": "hr"},
        ),
        Document(
            document_id="doc-acme-tenant",
            tenant_id="acme",
            owner_id="u-bob",
            visibility=Visibility.tenant,
            content="ACME internal finance memo: Q3 revenue and margins summary.",
            metadata={"title": "ACME Q3 Finance", "category": "finance"},
        ),
        Document(
            document_id="doc-acme-private-alice",
            tenant_id="acme",
            owner_id="u-alice",
            visibility=Visibility.private,
            content="Alice private notes: personal salary negotiation talking points.",
            metadata={"title": "Alice Notes", "category": "personal"},
        ),
        Document(
            document_id="doc-globex-public",
            tenant_id="globex",
            owner_id="u-erin",
            visibility=Visibility.public,
            content="Globex public brochure and product overview for customers.",
            metadata={"title": "Globex Brochure", "category": "marketing"},
        ),
        Document(
            document_id="doc-globex-tenant",
            tenant_id="globex",
            owner_id="u-erin",
            visibility=Visibility.tenant,
            content="Globex internal roadmap: Project Nautilus and the Initech acquisition.",
            metadata={"title": "Globex Roadmap", "category": "strategy"},
        ),
        Document(
            document_id="doc-globex-private-dave",
            tenant_id="globex",
            owner_id="u-dave",
            visibility=Visibility.private,
            content="Dave private notes: draft performance improvement plan.",
            metadata={"title": "Dave Notes", "category": "personal"},
        ),
    ]
