"""Extraction task models."""

import uuid
from enum import StrEnum

import pydantic

from app.models.socialnetwork import SocialNetwork


class _ExtractPostDetailsTaskConfig(pydantic.BaseModel):
    account_id: str
    post_id: str


class _ExtractPostListTaskConfig(pydantic.BaseModel):
    account_id: str
    published_after: pydantic.AwareDatetime
    published_before: pydantic.AwareDatetime


class _ExtractAccountTaskConfig(pydantic.BaseModel):
    account_id: str


ExtractionTaskConfig = (
    _ExtractPostDetailsTaskConfig | _ExtractPostListTaskConfig | _ExtractAccountTaskConfig
)


class ExtractionTaskType(StrEnum):
    """Types of extraction tasks."""

    EXTRACT_ACCOUNT = "extract-account"
    EXTRACT_POST_LIST = "extract-post-list"
    EXTRACT_POST_DETAILS = "extract-post-details"


class ExtractionTaskStatus(StrEnum):
    """Available task statuses."""

    AVAILABLE = "AVAILABLE"
    ACQUIRED = "ACQUIRED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ExtractionTask(pydantic.BaseModel):
    """Extraction task models."""

    uid: uuid.UUID | None = None
    social_network: SocialNetwork
    type: ExtractionTaskType
    task_config: ExtractionTaskConfig
    status: ExtractionTaskStatus | None = None
    visible_at: pydantic.AwareDatetime | None = None
    error: str | None = None


class ExtractionTaskResponse(pydantic.BaseModel):
    """Extraction task response model."""

    task_uid: uuid.UUID | None = None
    social_network: SocialNetwork | None = None
    visible_at: pydantic.AwareDatetime | None = None
    type: ExtractionTaskType | None = None
    task_config: ExtractionTaskConfig | None = None
    error: str | None = None


class MarkTaskFailedPayload(pydantic.BaseModel):
    """Payload for MarkFailed endpoint."""

    error: str | None


class RecycleFailedTasksResponse(pydantic.BaseModel):
    """Response model for recycle failed tasks endpoint."""

    recycled_count: int


class RecycleExpiredTasksResponse(pydantic.BaseModel):
    """Response model for recycle expired tasks endpoint."""

    recycled_count: int


class StatusCount(pydantic.BaseModel):
    """Count for a specific status."""

    status: str
    count: int


class TaskTypeCount(pydantic.BaseModel):
    """Count for a specific task type."""

    type: str
    count: int


class NetworkCount(pydantic.BaseModel):
    """Count for a specific social network."""

    social_network: str
    count: int


class DetailedStats(pydantic.BaseModel):
    """Detailed stats for a combination of task type, network, and status."""

    type: str
    social_network: str
    status: str
    count: int


class ExtractionTaskStatsResponse(pydantic.BaseModel):
    """Response model for extraction task stats endpoint."""

    global_stats: dict
    detailed_stats: list[DetailedStats]
