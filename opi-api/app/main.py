from fastapi import FastAPI, APIRouter

from app.backend.routing import router
from app.backend.ping import router as ping_router


app = FastAPI(title="Observatoire pratique influence API")

main_router = APIRouter()
app.include_router(main_router)
app.include_router(router.router)
app.include_router(ping_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
