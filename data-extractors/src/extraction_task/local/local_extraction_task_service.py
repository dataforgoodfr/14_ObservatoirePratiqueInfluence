import datetime
from typing import Optional
from extraction_task.local.account_repository import Account, AccountRepository
from extraction_task.local.post_repository import (
    PostDetails,
    PostRepository,
)
from extraction_task.local.task_repository import TaskRepository
from extraction_task.extraction_task_service import ExtractionTaskService
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskStatus,
    ExtractionTaskType,
)
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.extraction_task_result import (
    AccountExtractionResult,
    PostDetailsExtractionResult,
    PostListExtractionResult,
    ExtractionTaskResult,
)


from extraction_task.social_network import SocialNetwork


class LocalExtractionTaskService(ExtractionTaskService):
    """
    A local implementation of ExtractionTaskService
    using local storage for tasks and results.
    This is a temporary implementation until the API backend is ready
    """

    _task_repository: TaskRepository

    _account_repository: AccountRepository
    _post_repository: PostRepository

    _create_post_details_tasks: bool

    def __init__(
        self,
        task_repository: TaskRepository,
        account_repository: AccountRepository,
        post_repository: PostRepository,
        create_post_details_tasks: bool = True,
    ):
        self._task_repository = task_repository
        self._account_repository = account_repository
        self._post_repository = post_repository

        self._create_post_details_tasks = create_post_details_tasks

    def acquire_next_task(
        self, social_network: SocialNetwork
    ) -> Optional[ExtractionTask]:
        task = self._task_repository.get_first_acquirable_task(social_network)

        if task is None:
            return None

        task.status = ExtractionTaskStatus.ACQUIRED
        task.visible_at = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(minutes=60)
        self._task_repository.upsert(task)

        return task

    def mark_task_completed(
        self, task: ExtractionTask, task_result: ExtractionTaskResult
    ) -> None:
        task_config = task.task_config
        refetched_task = self._task_repository.find_by_id(task.id)
        if refetched_task is None:
            raise Exception("Task does not exist")

        if not refetched_task.is_acquired_and_current():
            raise Exception("Task is not acquired or acquisition timedout")

        if task.type == ExtractionTaskType.EXTRACT_ACCOUNT:
            assert isinstance(task_result, AccountExtractionResult)
            assert isinstance(task_config, ExtractAccountTaskConfig)
            self._account_repository.upsertAccount(
                Account(
                    social_network=task.social_network,
                    account_id=task_config.account_id,
                    handle=task_result.handle,
                    account_extraction_date=task_result.data_extraction_date,
                    description=task_result.description,
                    follower_count=task_result.follower_count,
                    following_count=task_result.following_count,
                    post_count=task_result.post_count,
                    view_count=task_result.view_count,
                    like_count=task_result.like_count,
                    categories=task_result.categories,
                )
            )
        elif task.type == ExtractionTaskType.EXTRACT_POST_LIST:
            assert isinstance(task_result, PostListExtractionResult)
            assert isinstance(task_config, ExtractPostListTaskConfig)
            self._upsert_posts(
                task_result.posts, task.social_network, task_config.account_id
            )

        elif task.type == ExtractionTaskType.EXTRACT_POST_DETAILS:
            assert isinstance(task_result, PostDetailsExtractionResult)
            assert isinstance(task_config, ExtractPostDetailsTaskConfig)
            self._upsert_posts(
                [task_result], task.social_network, task_config.account_id
            )
        else:
            raise Exception("Unexpected result")

        refetched_task.visible_at = None
        refetched_task.error = None
        refetched_task.status = ExtractionTaskStatus.COMPLETED
        self._task_repository.upsert(refetched_task)
        return

    def _upsert_posts(
        self,
        posts: list[PostDetailsExtractionResult],
        social_network: SocialNetwork,
        account_id: str,
    ) -> None:
        post_details_list = [
            PostDetails(
                social_network=social_network,
                account_id=account_id,
                post_id=post.post_id,
                post_extraction_date=post.data_extraction_date,
                post_url=post.post_url,
                title=post.title,
                description=post.description,
                comment_count=post.comment_count,
                view_count=post.view_count,
                repost_count=post.repost_count,
                like_count=post.like_count,
                share_count=post.share_count,
                categories=post.categories,
                tags=post.tags,
                sn_has_paid_placement=post.sn_has_paid_placement,
                sn_brand=post.sn_brand,
                post_type=post.post_type,
                text_content=post.text_content,
            )
            for post in posts
        ]
        self._post_repository.upsert_post_list(post_details_list)

    def mark_task_failed(self, task: ExtractionTask, task_error: str) -> None:
        refetched_task = self._task_repository.find_by_id(task.id)
        if refetched_task is None:
            raise Exception("Task does not exist")

        if not refetched_task.is_acquired_and_current():
            raise Exception(
                f"Task is not acquired or acquisition timed out - status:{task.status}, visible_at:{task.visible_at}"
            )

        refetched_task.status = ExtractionTaskStatus.FAILED
        refetched_task.error = task_error
        refetched_task.visible_at = None

        self._task_repository.upsert(refetched_task)
        return
