import fastapi

from app.backend.routing.endpoints import extraction_task, influencer, social_network

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
    "/extraction-task/recycle-failed",
    endpoint=extraction_task.recycle_failed_tasks,
    methods=["POST"],
    description="Recycle all failed tasks back to available status",
)
router.add_api_route(
    "/extraction-task/recycle-expired",
    endpoint=extraction_task.recycle_expired_tasks,
    methods=["POST"],
    description="Recycle all acquired tasks that have passed their acquisition limit",
)
router.add_api_route(
    "/extraction-task/{task_uid}/mark-failed/",
    endpoint=extraction_task.mark_failed,
    methods=["POST"],
    description="Mark Failed",
)

router.add_api_route(
    "/extraction-task/{task_uid}/mark-completed",
    endpoint=extraction_task.mark_completed,
    methods=["POST"],
    description="Mark Completed",
)
router.add_api_route(
    "/extraction-task/",
    endpoint=extraction_task.register_tasks,
    methods=["POST"],
    description="Register tasks",
)
router.add_api_route(
    "/posts/",
    endpoint=social_network.upsert_posts,
    methods=["POST"],
    description="Upsert account posts",
)
router.add_api_route(
    "/accounts/",
    endpoint=social_network.upsert_accounts,
    methods=["POST"],
    description="Upsert accounts data",
)
router.add_api_route(
    "/extraction-task/stats",
    endpoint=extraction_task.get_extraction_task_stats,
    methods=["GET"],
    description="Get statistics on extraction tasks with optional filters",
)
