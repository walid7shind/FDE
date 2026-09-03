from __future__ import annotations

import itertools
import time

from app.domain.models import AuditLog


class AuditRepository:
    def __init__(self) -> None:
        self._logs: list[AuditLog] = []
        self._counter = itertools.count(1)

    def record(
        self, tenant_id: str, user_id: str, action: str, target_id: str | None = None
    ) -> None:
        self._logs.append(
            AuditLog(
                log_id=f"log-{next(self._counter)}",
                tenant_id=tenant_id,
                user_id=user_id,
                action=action,
                target_id=target_id,
                timestamp=time.time(),
            )
        )

    def list_for_tenant(self, tenant_id: str) -> list[AuditLog]:
        return [entry for entry in self._logs if entry.tenant_id == tenant_id]

    def all(self) -> list[AuditLog]:
        return list(self._logs)
