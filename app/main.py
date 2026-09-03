from __future__ import annotations

from fastapi import FastAPI

from app.api import admin, answer, documents, search
from app.state import AppState, build_state, set_app_state


def create_app(state: AppState | None = None) -> FastAPI:
    application = FastAPI(title="Enterprise RAG API", version="0.1.0")
    set_app_state(state or build_state())
    application.include_router(documents.router)
    application.include_router(search.router)
    application.include_router(answer.router)
    application.include_router(admin.router)
    return application


app = create_app()
