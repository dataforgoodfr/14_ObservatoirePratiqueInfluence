import datetime
from enum import StrEnum
from pydantic import AwareDatetime, BaseModel
from extraction_task.extraction_task_config import ExtractionTaskConfig
from extraction_task.social_network import SocialNetwork
from typing import Optional
import uuid


class ExtractionTaskType(StrEnum):
    EXTRACT_ACCOUNT = "extract-account"
    EXTRACT_POST_LIST = "extract-post-list"
    EXTRACT_POST_DETAILS = "extract-post-details"


class ExtractionTaskStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    ACQUIRED = "ACQUIRED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ExtractionTask(BaseModel):
    id: uuid.UUID
    social_network: SocialNetwork
    type: ExtractionTaskType
    task_config: ExtractionTaskConfig
    status: ExtractionTaskStatus
    visible_at: Optional[AwareDatetime]
    error: Optional[str]

    def is_acquirable(self) -> bool:
        return self.status == ExtractionTaskStatus.AVAILABLE or (
            self.status == ExtractionTaskStatus.ACQUIRED
            and self.visible_at is not None
            and self.visible_at < datetime.datetime.now(datetime.timezone.utc)
        )

    def is_acquired_and_current(self) -> bool:
        return (
            self.status == ExtractionTaskStatus.ACQUIRED
            and self.visible_at is not None
            and self.visible_at > datetime.datetime.now(datetime.timezone.utc)
        )
