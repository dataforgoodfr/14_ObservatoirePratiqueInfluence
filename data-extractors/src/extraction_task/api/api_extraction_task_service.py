import logging

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
    Account,
    Post as ApiPost,
    MarkFailedPayload,
)

from extraction_task.social_network import SocialNetwork as DomainSocialNetwork

LOGGER = logging.getLogger(__name__)


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

        LOGGER.info("Upserting data...")
        # Handle different task types
        if isinstance(task_result, AccountExtractionResult):
            assert isinstance(task.task_config, DomainExtractAccountTaskConfig)
            self._upsert_account(
                task_result, task.task_config.account_id, task.social_network
            )
        elif isinstance(task_result, PostListExtractionResult):
            assert isinstance(task.task_config, DomainExtractPostListTaskConfig)
            self._upsert_posts(
                task_result.posts, task.task_config.account_id, task.social_network
            )
        elif isinstance(task_result, PostDetailsExtractionResult):
            assert isinstance(task.task_config, DomainExtractPostDetailsTaskConfig)
            self._upsert_posts(
                [task_result], task.task_config.account_id, task.social_network
            )
        else:
            raise ValueError(f"Unknown task result type: {type(task_result)}")

        # Mark task as completed
        LOGGER.info("Marking extraction task complete")
        self._api.mark_completed_extraction_task_task_uid_mark_completed_post(
            task.id,
        )

    def _upsert_account(
        self,
        task_result: AccountExtractionResult,
        account_id: str,
        social_network: str,
    ) -> None:
        """Upsert account data to the API."""
        account = Account(
            account_extracted_at=task_result.data_extraction_date,
            account_id=account_id,
            social_network=social_network,
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

    def _upsert_posts(
        self,
        post_details_list: list[PostDetailsExtractionResult],
        account_id: str,
        social_network: DomainSocialNetwork,
    ) -> None:
        """Upsert post data to the API."""

        api_posts: list[ApiPost] = [
            ApiPost(
                post_extracted_at=post_details.data_extraction_date,
                social_network=social_network,
                account_id=account_id,
                post_id=post_details.post_id,
                post_url=post_details.post_url,
                title=post_details.title,
                description=post_details.description,
                comment_count=post_details.comment_count,
                view_count=post_details.view_count,
                repost_count=post_details.repost_count,
                like_count=post_details.like_count,
                share_count=post_details.share_count,
                categories=post_details.categories,
                tags=post_details.tags,
                sn_has_paid_placement=post_details.sn_has_paid_placement,
                sn_brand=post_details.sn_brand,
                post_type=post_details.post_type,
                text_content=post_details.text_content,
            )
            for post_details in post_details_list
        ]

        chunk_size = 300
        api_posts_chunks = [
            api_posts[i : i + chunk_size] for i in range(0, len(api_posts), chunk_size)
        ]

        for chunkIndex, chunk in enumerate(api_posts_chunks):
            LOGGER.info(
                "upserting post chunk %s/%s", chunkIndex + 1, len(api_posts_chunks)
            )
            self._api.upsert_posts_posts_post(chunk)
