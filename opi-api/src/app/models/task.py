from enum import StrEnum

import uuid

import pydantic

from typing import Optional, Union

from app.models.socialnetwork import SocialNetwork


class ExtractPostDetailsTaskConfig(pydantic.BaseModel):
    post_id: str


class ExtractPostListTaskConfig(pydantic.BaseModel):
    account_id: str
    published_after: pydantic.AwareDatetime
    published_before: pydantic.AwareDatetime


class ExtractAccountTaskConfig(pydantic.BaseModel):
    # FIXME this should be an account id rather than a handle
    account_id: str

ExtractionTaskConfig = Union[
    ExtractPostDetailsTaskConfig, ExtractPostListTaskConfig, ExtractAccountTaskConfig
]

class ExtractionTaskType(StrEnum):
    EXTRACT_ACCOUNT = "extract-account"
    EXTRACT_POST_LIST = "extract-post-list"
    EXTRACT_POST_DETAILS = "extract-post-details"


class ExtractionTaskStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    ACQUIRED = "ACQUIRED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ExtractionTask(pydantic.BaseModel):
    uid: Optional[uuid.UUID] = None
    social_network: SocialNetwork
    type: ExtractionTaskType
    task_config: ExtractionTaskConfig
    status: Optional[ExtractionTaskStatus] = None
    visible_until: Optional[pydantic.AwareDatetime] = None
    error: Optional[str] = None


class ExtractionTaskResponse(pydantic.BaseModel):
    task_uid: Optional[uuid.UUID] = None
    social_network: Optional[SocialNetwork] = None
    visible_until: Optional[pydantic.AwareDatetime] = None
    type: Optional[ExtractionTaskType] = None
    task_config: Optional[ExtractionTaskConfig] = None
    error: Optional[str] = None
