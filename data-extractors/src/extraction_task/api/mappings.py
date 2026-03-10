"""Mapping utilities for converting between domain and API models."""

import logging

from api_client.models import (
    ExtractionTaskType as ApiExtractionTaskType,
    SocialNetwork as ApiSocialNetwork,
    ExtractionTask as ApiExtractionTask,
    ExtractAccountTaskConfig as ApiExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig as ApiExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig as ApiExtractPostListTaskConfig,
    TaskConfig as ApiTaskConfig,
    ExtractionTaskStatus as ApiExtractionTaskStatus,
)
from api_client.models.extraction_task_response import (
    ExtractionTaskResponse as ApiExtractionTaskResponse,
)
from extraction_task.extraction_task import (
    ExtractionTaskType as DomainExtractionTaskType,
    ExtractionTaskStatus as DomainExtractionTaskStatus,
)
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig as DomainExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig as DomainExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig as DomainExtractPostListTaskConfig,
    ExtractionTaskConfig,
)
import datetime
from extraction_task.social_network import SocialNetwork as DomainSocialNetwork

from extraction_task.extraction_task import ExtractionTask as DomainExtractionTask

LOGGER = logging.getLogger(__name__)


def to_domain_social_network(
    api_social_network: ApiSocialNetwork,
) -> DomainSocialNetwork:
    return DomainSocialNetwork(api_social_network.value)


def to_api_social_network(
    domain_social_network: DomainSocialNetwork,
) -> ApiSocialNetwork:
    return ApiSocialNetwork(domain_social_network.value)


def to_domain_task_type(
    api_task_type: ApiExtractionTaskType,
) -> DomainExtractionTaskType:
    return DomainExtractionTaskType(api_task_type.value)


def to_api_task_type(
    domain_task_type: DomainExtractionTaskType,
) -> ApiExtractionTaskType:
    return ApiExtractionTaskType(domain_task_type.value)


def to_api_extractions_tasks(
    tasks: list[DomainExtractionTask],
) -> list[ApiExtractionTask]:
    result = []
    for task in tasks:
        # Convert task_config based on its type (using domain model types)
        # Use type: ignore to handle Union type assignment in different branches
        api_config: (
            ApiExtractAccountTaskConfig
            | ApiExtractPostDetailsTaskConfig
            | ApiExtractPostListTaskConfig
        )
        if isinstance(task.task_config, DomainExtractAccountTaskConfig):
            api_config = ApiExtractAccountTaskConfig(
                account_id=task.task_config.account_id
            )
        elif isinstance(task.task_config, DomainExtractPostDetailsTaskConfig):
            api_config = ApiExtractPostDetailsTaskConfig(
                account_id=task.task_config.account_id,
                post_id=task.task_config.post_id,
            )
        elif isinstance(task.task_config, DomainExtractPostListTaskConfig):
            api_config = ApiExtractPostListTaskConfig(
                account_id=task.task_config.account_id,
                published_after=task.task_config.published_after,
                published_before=task.task_config.published_before,
            )
        else:
            raise ValueError(f"Unknown task config type: {type(task.task_config)}")

        visible_at = task.visible_at

        api_task = ApiExtractionTask(
            uid=task.id,
            social_network=to_api_social_network(task.social_network),
            type=to_api_task_type(task.type),
            task_config=ApiTaskConfig(actual_instance=api_config),
            status=ApiExtractionTaskStatus(task.status.value),
            visible_at=visible_at,
            error=task.error,
        )
        result.append(api_task)
    return result


def to_domain_extractions_task(
    task_response: ApiExtractionTaskResponse,
) -> DomainExtractionTask:
    assert task_response.task_uid is not None
    assert task_response.social_network is not None
    assert task_response.type is not None
    assert task_response.task_config is not None

    # Determine domain config based on the type
    domain_task_type = to_domain_task_type(task_response.type)
    domain_config: ExtractionTaskConfig

    assert task_response.task_config.actual_instance is not None
    if domain_task_type == DomainExtractionTaskType.EXTRACT_POST_DETAILS:
        assert isinstance(
            task_response.task_config.actual_instance, ApiExtractPostDetailsTaskConfig
        )
        domain_config = to_domain_extract_post_details_task_config(
            task_response.task_config.actual_instance
        )
    elif domain_task_type == DomainExtractionTaskType.EXTRACT_POST_LIST:
        assert isinstance(
            task_response.task_config.actual_instance, ApiExtractPostListTaskConfig
        )
        domain_config = to_domain_extract_post_list_task_config(
            task_response.task_config.actual_instance
        )
    elif domain_task_type == DomainExtractionTaskType.EXTRACT_ACCOUNT:
        assert isinstance(
            task_response.task_config.actual_instance, ApiExtractAccountTaskConfig
        )
        domain_config = to_domain_extract_account_task_config(
            task_response.task_config.actual_instance
        )

    else:
        raise ValueError(f"Unknown task type: {domain_task_type}")

    # Convert visible_at to aware datetime if present
    visible_at = task_response.visible_at
    if visible_at:
        # Make it timezone-aware (UTC)
        visible_at = visible_at.replace(tzinfo=datetime.timezone.utc)

    return DomainExtractionTask(
        id=task_response.task_uid,
        social_network=to_domain_social_network(task_response.social_network),
        type=domain_task_type,
        task_config=domain_config,
        status=DomainExtractionTaskStatus.ACQUIRED,
        visible_at=visible_at,
        error=task_response.error,
    )


def to_domain_extract_account_task_config(
    api_config: ApiExtractAccountTaskConfig,
) -> DomainExtractAccountTaskConfig:
    return DomainExtractAccountTaskConfig(account_id=api_config.account_id)


def to_domain_extract_post_details_task_config(
    api_config: ApiExtractPostDetailsTaskConfig,
) -> DomainExtractPostDetailsTaskConfig:
    return DomainExtractPostDetailsTaskConfig(
        account_id=api_config.account_id, post_id=api_config.post_id
    )


def to_domain_extract_post_list_task_config(
    api_config: ApiExtractPostListTaskConfig,
) -> DomainExtractPostListTaskConfig:

    return DomainExtractPostListTaskConfig(
        account_id=api_config.account_id,
        published_after=api_config.published_after,
        published_before=api_config.published_before,
    )
