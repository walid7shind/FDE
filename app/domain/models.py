from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Role(StrEnum):
    employee = "employee"
    manager = "manager"
    admin = "admin"


class Visibility(StrEnum):
    private = "private"
    tenant = "tenant"
    public = "public"


class User(BaseModel):
    user_id: str
    tenant_id: str
    role: Role


class Document(BaseModel):
    document_id: str
    tenant_id: str
    owner_id: str
    visibility: Visibility
    content: str
    metadata: dict[str, str] = Field(default_factory=dict)


class AuditLog(BaseModel):
    log_id: str
    tenant_id: str
    user_id: str
    action: str
    target_id: str | None = None
    timestamp: float
