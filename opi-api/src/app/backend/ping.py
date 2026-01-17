from fastapi import APIRouter
from fastapi.responses import Response


router = APIRouter(tags=["Ping"])


@router.get("/ping")
async def ping() -> Response:
    """Ping endpoint"""

    return Response(content="pong")
