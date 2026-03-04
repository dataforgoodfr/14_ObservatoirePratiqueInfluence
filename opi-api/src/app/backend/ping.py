"""Ping endpoint."""

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app._auth import validate_api_key

router = APIRouter(tags=["Ping"])
API_KEY = Depends(validate_api_key)

@router.get("/ping")
async def ping(api_key: str = API_KEY) -> Response:
    """Ping endpoint."""
    return Response(content="pong")
