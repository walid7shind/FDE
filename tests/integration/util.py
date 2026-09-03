from __future__ import annotations

import httpx
from app.main import create_app
from app.state import AppState


def build_client(state: AppState | None = None) -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=create_app(state))
    return httpx.AsyncClient(transport=transport, base_url="http://testserver")
