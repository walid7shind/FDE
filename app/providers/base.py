from __future__ import annotations


class ProviderError(RuntimeError):
    """Raised when a downstream model provider is unavailable or misbehaving."""
