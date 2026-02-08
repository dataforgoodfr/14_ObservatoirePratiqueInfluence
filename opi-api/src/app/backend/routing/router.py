import fastapi

from app.backend.routing.endpoints import influencer
from app.backend.routing.endpoints import extraction_task


router = fastapi.APIRouter()
router.add_api_route(
    "/influencer/{username}",
    endpoint=influencer.get_influencer_accounts,
    methods=["GET"],
    description="Get social network accounts for an influencer",
)
router.add_api_route(
    "/extraction-task/acquire",
    endpoint=extraction_task.acquire_available_task,
    methods=["POST"],
    description="Get available task and switch its status to acquired",
)
router.add_api_route(
    "/extraction-task/{task_id}",
    endpoint=extraction_task.update_task,
    methods=["PATCH"],
    description="Update existing tasks",
)
router.add_api_route(
    "/extraction-task/",
    endpoint=extraction_task.register_tasks,
    methods=["POST"],
    description="Register tasks",
)
