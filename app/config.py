from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    embedding_dim: int = 64
    default_top_k: int = 5
    max_top_k: int = 50
    llm_timeout_seconds: float = 2.0
    llm_max_retries: int = 2


settings = Settings()
