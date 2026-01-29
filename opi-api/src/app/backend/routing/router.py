import fastapi

from app.backend.routing.endpoints import influencer


router = fastapi.APIRouter()
router.add_api_route(
    "/influencer/{username}",
    endpoint=influencer.get_influencer_accounts,
    methods=["GET"],
    description="Get social network accounts for an influencer",
)
