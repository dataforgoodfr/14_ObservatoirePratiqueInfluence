import datetime
from typing import Optional
import uuid
from extraction_task.local.task_repository import TaskRepository
from extraction_task.local.task_result_repository import (
    TaskResultRepository,
)
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

    _result_repository: TaskResultRepository
    _create_post_details_tasks: bool

    def __init__(
        self,
        task_repository: TaskRepository,
        result_repository: TaskResultRepository,
        create_post_details_tasks: bool = True,
    ):
        self._task_repository = task_repository
        self._result_repository = result_repository
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
            self._result_repository.persist_extract_account_result(
                task.id, task_result, task.task_config
            )
        elif (
            task.type == ExtractionTaskType.EXTRACT_POST_LIST
            and isinstance(task_result, PostListExtractionResult)
            and isinstance(task.task_config, ExtractPostListTaskConfig)
        ):
            self._result_repository.persist_extract_post_list_result(
                task.id, task_result, task.task_config
            )
            if self._create_post_details_tasks:
                # create post detail
                for post in task_result.posts:
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
            self._result_repository.persist_extract_post_details_result(
                task.id, task_result, task.task_config
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
            raise Exception("Task is not acquired or acquisition timedout")

        task.status = ExtractionTaskStatus.FAILED
        task.error = task_error
        task.visible_at = None

        self._task_repository.upsert(task)
        return
