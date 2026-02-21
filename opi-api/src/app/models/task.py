"""Extraction task models."""

import uuid
from enum import StrEnum

import pydantic

from app.models.socialnetwork import SocialNetwork


class _ExtractPostDetailsTaskConfig(pydantic.BaseModel):
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
