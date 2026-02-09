import datetime
from typing import Optional
import uuid
from extraction_task.local.account_repository import Account, AccountRepository
from extraction_task.local.post_repository import (
    PostDetails,
    PostListItem,
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
        ) + datetime.timedelta(minutes=15)
        self._task_repository.upsert(task)

        return task

    def mark_task_completed(
        self, task_id: uuid.UUID, task_result: ExtractionTaskResult
    ) -> None:
        task = self._task_repository.find_by_id(task_id)
        if task is None:
            raise Exception("Task does not exist")

        if not task.is_acquired_and_current():
            raise Exception("Task is not acquired or acquisition timedout")

        task.visible_at = None
        task.error = None
        task.status = ExtractionTaskStatus.COMPLETED

        if (
            task.type == ExtractionTaskType.EXTRACT_ACCOUNT
            and isinstance(task_result, AccountExtractionResult)
            and isinstance(task.task_config, ExtractAccountTaskConfig)
        ):
            self._account_repository.upsertAccount(
                Account(
                    social_network=task.social_network,
                    account_id=task.task_config.account_id,
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
        elif (
            task.type == ExtractionTaskType.EXTRACT_POST_LIST
            and isinstance(task_result, PostListExtractionResult)
            and isinstance(task.task_config, ExtractPostListTaskConfig)
        ):
            for post in task_result.posts:
                self._post_repository.upsert_post_list_item(
                    PostListItem(
                        social_network=task.social_network,
                        post_id=post.post_id,
                        account_id=task.task_config.account_id,
                    )
                )

                if self._create_post_details_tasks:
                    # create post detail
                    self._task_repository.upsert(
                        ExtractionTask(
                            id=uuid.uuid4(),
                            social_network=task.social_network,
                            type=ExtractionTaskType.EXTRACT_POST_DETAILS,
                            task_config=ExtractPostDetailsTaskConfig(
                                post_id=post.post_id
                            ),
                            status=ExtractionTaskStatus.AVAILABLE,
                            error=None,
                            visible_at=None,
                        )
                    )
        elif (
            task.type == ExtractionTaskType.EXTRACT_POST_DETAILS
            and isinstance(task_result, PostDetailsExtractionResult)
            and isinstance(task.task_config, ExtractPostDetailsTaskConfig)
        ):
            self._post_repository.upsert_post_details(
                PostDetails(
                    social_network=task.social_network,
                    post_id=task.task_config.post_id,
                    post_extraction_date=task_result.data_extraction_date,
                    title=task_result.title,
                    description=task_result.description,
                    comment_count=task_result.comment_count,
                    view_count=task_result.view_count,
                    repost_count=task_result.repost_count,
                    like_count=task_result.like_count,
                    share_count=task_result.share_count,
                    categories=task_result.categories,
                    tags=task_result.tags,
                    sn_has_paid_placement=task_result.sn_has_paid_placement,
                    sn_brand=task_result.sn_brand,
                    post_type=task_result.post_type,
                    text_content=task_result.text_content,
                )
            )
        else:
            raise Exception("Unexpected result")
        self._task_repository.upsert(task)
        return

    def mark_task_failed(self, task_id: uuid.UUID, task_error: str) -> None:
        task = self._task_repository.find_by_id(task_id)
        if task is None:
            raise Exception("Task does not exist")

        if not task.is_acquired_and_current():
            raise Exception(
                f"Task is not acquired or acquisition timed out - status:{task.status}, visible_at:{task.visible_at}"
            )

        task.status = ExtractionTaskStatus.FAILED
        task.error = task_error
        task.visible_at = None

        self._task_repository.upsert(task)
        return
