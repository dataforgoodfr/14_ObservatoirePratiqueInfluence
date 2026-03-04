import fastapi
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app._config import settings

api_key_header = HTTPBearer()
credentials = fastapi.Depends(api_key_header)

def validate_api_key(
    credentials: HTTPAuthorizationCredentials = credentials,
) -> str:
    key = credentials.credentials
    if key != settings.api_key:
        raise fastapi.HTTPException(status_code=401, detail="Invalid API Key")

    return key
