from uuid import UUID

from extraction_task.api import api_client
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskStatus,
    ExtractionTaskType,
)
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
    ExtractionTaskConfig,
)
from extraction_task.extraction_task_result import (
    AccountExtractionResult,
    ExtractionTaskResult,
    PostDetailsExtractionResult,
    PostListExtractionResult,
)
from extraction_task.extraction_task_service import ExtractionTaskService
from extraction_task.social_network import SocialNetwork as DomainSocialNetwork


class ApiExtractionTaskService(ExtractionTaskService):
    """Service to communicate with the HTTP API for extraction tasks.

    Uses the typed ApiClient to interact with the OPI API endpoints.
    Maps between API models and domain models.
    """

    def __init__(self, api_url: str, api_token: str) -> None:
        self._client = api_client.ApiClient(api_url, api_token)

    def _to_domain_social_network(
        self, api_social_network: api_client.SocialNetwork
    ) -> DomainSocialNetwork:
        """Convert API social network to domain social network."""
        return DomainSocialNetwork(api_social_network.value)

    def _to_api_social_network(
        self, domain_social_network: DomainSocialNetwork
    ) -> api_client.SocialNetwork:
        """Convert domain social network to API social network."""
        return api_client.SocialNetwork(domain_social_network.value)

    def _to_domain_task_type(
        self, api_task_type: api_client.ExtractionTaskType
    ) -> ExtractionTaskType:
        """Convert API task type to domain task type."""
        return ExtractionTaskType(api_task_type.value)

    def _to_api_task_type(
        self, domain_task_type: ExtractionTaskType
    ) -> api_client.ExtractionTaskType:
        """Convert domain task type to API task type."""
        return api_client.ExtractionTaskType(domain_task_type.value)

    def _to_domain_task_status(
        self, api_task_status: api_client.ExtractionTaskStatus
    ) -> ExtractionTaskStatus:
        """Convert API task status to domain task status."""
        return ExtractionTaskStatus(api_task_status.value)

    def _to_api_task_status(
        self, domain_task_status: ExtractionTaskStatus
    ) -> api_client.ExtractionTaskStatus:
        """Convert domain task status to API task status."""
        return api_client.ExtractionTaskStatus(domain_task_status.value)

    def _task_config_to_dict(self, task_config: ExtractionTaskConfig) -> dict:
        """Convert domain task config to dict for API."""
        return task_config.model_dump()

    def _parse_task_config(
        self, task_type: ExtractionTaskType, config: dict
    ) -> ExtractionTaskConfig:
        """Parse task config from API response based on task type."""
        if task_type == ExtractionTaskType.EXTRACT_ACCOUNT:
            return ExtractAccountTaskConfig(**config)
        elif task_type == ExtractionTaskType.EXTRACT_POST_LIST:
            return ExtractPostListTaskConfig(**config)
        elif task_type == ExtractionTaskType.EXTRACT_POST_DETAILS:
            return ExtractPostDetailsTaskConfig(**config)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def acquire_next_task(
        self, social_network: DomainSocialNetwork
    ) -> ExtractionTask | None:
        """Acquire the next available task from the API.

        Args:
            social_network: The social network to filter tasks by.

        Returns:
            The acquired task, or None if no task is available.
        """
        api_social_network = self._to_api_social_network(social_network)
        response = self._client.acquire_task(api_social_network)

        # Check if no task is available
        if response.error == "no-task-available":
            return None

        # Convert API response to domain model
        assert response.task_uid is not None
        assert response.social_network is not None
        assert response.type is not None
        assert response.task_config is not None

        task_config = self._parse_task_config(
            self._to_domain_task_type(response.type),
            response.task_config.model_dump(),
        )

        return ExtractionTask(
            id=response.task_uid,
            social_network=self._to_domain_social_network(response.social_network),
            type=self._to_domain_task_type(response.type),
            task_config=task_config,
            status=ExtractionTaskStatus.ACQUIRED,
            visible_at=response.visible_at,
            error=response.error,
        )

    def mark_task_failed(self, task: ExtractionTask, task_error: str) -> None:
        """Mark a task as failed."""
        self._client.update_task(
            task.id,
            api_client.ExtractionTaskStatus.FAILED,
        )

    def mark_task_completed(
        self, task: ExtractionTask, task_result: ExtractionTaskResult
    ) -> None:
        """Mark a task as completed and process the result."""
        social_network = task.social_network

        # Handle different task types
        if isinstance(task_result, AccountExtractionResult):
            assert isinstance(task.task_config, ExtractAccountTaskConfig)
            self._upsert_account(task_result, task.task_config, social_network)
        elif isinstance(task_result, PostListExtractionResult):
            assert isinstance(task.task_config, ExtractPostListTaskConfig)
            self._create_post_detail_tasks(
                task_result, task.task_config, social_network
            )
        elif isinstance(task_result, PostDetailsExtractionResult):
            assert isinstance(task.task_config, ExtractPostDetailsTaskConfig)
            self._upsert_post(task_result, task.task_config, social_network)
        else:
            raise ValueError(f"Unknown task result type: {type(task_result)}")

        # Mark task as completed
        self._client.update_task(
            task.id,
            api_client.ExtractionTaskStatus.COMPLETED,
        )

    def _upsert_account(
        self,
        task_result: AccountExtractionResult,
        task_config: ExtractAccountTaskConfig,
        social_network: DomainSocialNetwork,
    ) -> None:
        """Upsert account data to the API."""
        account = api_client.Account(
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

        self._client.upsert_accounts([account])

    def _create_post_detail_tasks(
        self,
        task_result: PostListExtractionResult,
        task_config: ExtractPostListTaskConfig,
        social_network: DomainSocialNetwork,
    ) -> None:
        """Create post detail tasks for each post in the list."""
        new_tasks: list[api_client.ExtractionTask] = []
        for post in task_result.posts:
            task = api_client.ExtractionTask(
                social_network=self._to_api_social_network(social_network),
                type=api_client.ExtractionTaskType.EXTRACT_POST_DETAILS,
                task_config=api_client._ExtractPostDetailsTaskConfig(
                    post_id=post.post_id,
                    account_id=task_config.account_id,
                ),
                status=api_client.ExtractionTaskStatus.AVAILABLE,
            )
            new_tasks.append(task)

        self._client.register_tasks(new_tasks)

    def _upsert_post(
        self,
        task_result: PostDetailsExtractionResult,
        task_config: ExtractPostDetailsTaskConfig,
        social_network: DomainSocialNetwork,
    ) -> None:
        """Upsert post data to the API."""
        # Note: task_config may not have account_id in the current domain model
        # This is a pre-existing issue in the codebase
        account_id = getattr(task_config, "account_id", "")

        post = api_client.Post(
            post_extracted_at=task_result.data_extraction_date,
            social_network=social_network.value,
            account_id=account_id,
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

        self._client.upsert_posts([post])
