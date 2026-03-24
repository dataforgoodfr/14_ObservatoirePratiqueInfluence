from api_client import api_client
from api_client.api import DefaultApi
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskType,
)
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig as DomainExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig as DomainExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig as DomainExtractPostListTaskConfig,
    ExtractionTaskConfig,
)
from extraction_task.extraction_task_result import (
    AccountExtractionResult,
    ExtractionTaskResult,
    PostDetailsExtractionResult,
    PostListExtractionResult,
)
from extraction_task.extraction_task_service import ExtractionTaskService
from extraction_task.api.mappings import (
    to_api_social_network,
    to_domain_extractions_task,
)

from api_client.models import (
    ExtractionTaskType as ApiExtractionTaskType,
    ExtractionTaskStatus as ApiExtractionTaskStatus,
    Account,
    Post,
    ExtractionTask as ApiExtractionTask,
    ExtractPostDetailsTaskConfig,
    TaskConfig,
    MarkFailedPayload,
)

from extraction_task.social_network import SocialNetwork as DomainSocialNetwork


class ApiExtractionTaskService(ExtractionTaskService):
    """Service to communicate with the HTTP API for extraction tasks.

    Uses the typed ApiClient to interact with the OPI API endpoints.
    Maps between API models and domain models.
    """

    def __init__(self, api_url: str, api_token: str) -> None:
        configuration = api_client.Configuration(access_token=api_token, host=api_url)
        self._client = api_client.ApiClient(configuration=configuration)
        self._api = DefaultApi(self._client)

    def acquire_next_task(
        self, social_network: DomainSocialNetwork
    ) -> ExtractionTask | None:

        response = self._api.acquire_available_task_extraction_task_acquire_post(
            to_api_social_network(social_network)
        )

        # Check if no task is available
        if response.error == "no-task-available":
            return None

        # Convert API response to domain model using the shared mapping function
        return to_domain_extractions_task(response)

    def mark_task_failed(self, task: ExtractionTask, task_error: str) -> None:
        """Mark a task as failed."""
        self._api.mark_failed_extraction_task_task_uid_mark_failed_post(
            task.id, mark_failed_payload=MarkFailedPayload(error=task_error)
        )

    def mark_task_completed(
        self, task: ExtractionTask, task_result: ExtractionTaskResult
    ) -> None:
        """Mark a task as completed and process the result."""
        social_network = task.social_network

        # Handle different task types
        if isinstance(task_result, AccountExtractionResult):
            assert isinstance(task.task_config, DomainExtractAccountTaskConfig)
            self._upsert_account(task_result, task.task_config, social_network)
        elif isinstance(task_result, PostListExtractionResult):
            assert isinstance(task.task_config, DomainExtractPostListTaskConfig)
            self._create_post_detail_tasks(
                task_result, task.task_config, social_network
            )
        elif isinstance(task_result, PostDetailsExtractionResult):
            assert isinstance(task.task_config, DomainExtractPostDetailsTaskConfig)
            self._upsert_post(task_result, task.task_config, social_network)
        else:
            raise ValueError(f"Unknown task result type: {type(task_result)}")

        # Mark task as completed
        self._api.mark_completed_extraction_task_task_uid_mark_completed_post(
            task.id,
        )

    def _upsert_account(
        self,
        task_result: AccountExtractionResult,
        task_config: DomainExtractAccountTaskConfig,
        social_network: DomainSocialNetwork,
    ) -> None:
        """Upsert account data to the API."""
        account = Account(
            account_extracted_at=task_result.data_extraction_date,
            account_id=task_config.account_id,
            social_network=social_network.value,
            handle=task_result.handle,
            description=task_result.description,
            follower_count=task_result.follower_count,
            following_count=task_result.following_count,
            post_count=task_result.post_count,
            view_count=task_result.view_count,
            like_count=task_result.like_count,
            categories=task_result.categories,
        )

        self._api.upsert_accounts_accounts_post([account])

    # Use shared mapping functions from extraction_task.mappings
    # _to_domain_social_network, _to_api_social_network, _to_domain_task_type, _to_api_task_type

    def _parse_task_config(
        self, task_type: ExtractionTaskType, config_dict: dict
    ) -> ExtractionTaskConfig:
        """Parse task config from API response to domain model."""
        if task_type == ExtractionTaskType.EXTRACT_ACCOUNT:
            return DomainExtractAccountTaskConfig(**config_dict)
        elif task_type == ExtractionTaskType.EXTRACT_POST_LIST:
            return DomainExtractPostListTaskConfig(**config_dict)
        elif task_type == ExtractionTaskType.EXTRACT_POST_DETAILS:
            return DomainExtractPostDetailsTaskConfig(**config_dict)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _create_post_detail_tasks(
        self,
        task_result: PostListExtractionResult,
        task_config: DomainExtractPostListTaskConfig,
        social_network: DomainSocialNetwork,
    ) -> None:
        """Create post detail tasks for each post in the list."""
        new_tasks: list[ApiExtractionTask] = []
        for post in task_result.posts:
            task = ApiExtractionTask(
                social_network=to_api_social_network(social_network),
                type=ApiExtractionTaskType.EXTRACT_MINUS_POST_MINUS_DETAILS,
                task_config=TaskConfig(
                    ExtractPostDetailsTaskConfig(
                        account_id=task_config.account_id,
                        post_id=post.post_id,
                    )
                ),
                status=ApiExtractionTaskStatus.AVAILABLE,
            )
            new_tasks.append(task)

        self._api.register_tasks_extraction_task_post(new_tasks)

    def _upsert_post(
        self,
        task_result: PostDetailsExtractionResult,
        task_config: DomainExtractPostDetailsTaskConfig,
        social_network: DomainSocialNetwork,
    ) -> None:
        """Upsert post data to the API."""
        # Note: task_config may not have account_id in the current domain model
        # This is a pre-existing issue in the codebase

        post = Post(
            post_extracted_at=task_result.data_extraction_date,
            social_network=social_network.value,
            account_id=task_config.account_id,
            post_id=task_config.post_id,
            post_url=task_result.post_url,
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

        self._api.upsert_posts_posts_post([post])
