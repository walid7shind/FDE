from __future__ import annotations

from app.domain.models import User


class UserRepository:
    def __init__(self, users: list[User]) -> None:
        self._users: dict[str, User] = {user.user_id: user for user in users}

    def get(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def all(self) -> list[User]:
        return list(self._users.values())
