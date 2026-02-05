from typing import Optional


from abc import ABC, abstractmethod
from uuid import UUID

from extraction_task.extraction_task import ExtractionTask
from extraction_task.extraction_task_result import (
    ExtractionTaskResult,
)
from extraction_task.social_network import SocialNetwork


class ExtractionTaskService(ABC):
    @abstractmethod
    def acquire_next_task(
        self, social_network: SocialNetwork
    ) -> Optional[ExtractionTask]:
        print("Abstract method1")
        return None

    @abstractmethod
    def mark_task_completed(
        self, task_id: UUID, task_result: ExtractionTaskResult
    ) -> None:
        print("Abstract method1")
        return None

    @abstractmethod
    def mark_task_failed(self, task_id: UUID, task_error: str) -> None:
        print("Abstract method1")
        return None
