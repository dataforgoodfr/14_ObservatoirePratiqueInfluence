"""Factory fro OPI API."""

from fastapi import APIRouter, FastAPI

from app.backend.ping import router as ping_router
from app.backend.routing import router


def create_app() -> FastAPI:
    """Create Fastapi app an inistialize routers."""
    app = FastAPI(title="Observatoire pratique influence API")

    main_router = APIRouter()
    app.include_router(main_router)
    app.include_router(router.router)
    app.include_router(ping_router)

    return app


app = create_app()
