import fastapi

from app.backend.routing.endpoints import account


router = fastapi.APIRouter()
router.add_api_route(
    "/account/{account_handle}",
    endpoint=account.get_accounts,
    methods=["GET"],
    description="Get social network accounts from handle",
)
