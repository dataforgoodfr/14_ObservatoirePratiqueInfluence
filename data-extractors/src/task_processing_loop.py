import logging

import time

import requests
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskType,
)
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.extraction_task_result import ExtractionTaskResult
from extraction_task.social_network import SocialNetwork
from data_extractors.data_extractor import DataExtractor
from extraction_task.extraction_task_service import ExtractionTaskService

logger = logging.getLogger(__name__)


class TaskProcessingLoop:
    _task_service: ExtractionTaskService
    _polling_interval: int
    _social_network: SocialNetwork
    _extractor: DataExtractor

    def __init__(
        self,
        task_repository: ExtractionTaskService,
        social_network: SocialNetwork,
        extractor: DataExtractor,
        polling_interval: int,
    ):
        self._social_network = social_network
        self._task_service = task_repository
        self._polling_interval = polling_interval
        self._extractor = extractor

    def run(self) -> None:
        public_ip = get_my_public_ip()
        logger.info("Public IP: " + public_ip)

        while True:
            logger.info("Attempting to acquire a task for %s", self._social_network)
            task = self._task_service.acquire_next_task(self._social_network)
            if task is None:
                logger.info(
                    "No tasks available - Sleeping %ss before next poll",
                    self._polling_interval,
                )
                time.sleep(self._polling_interval)
            else:
                logger.info(
                    "Successfully acquired task with id %s - Executing it",
                    task.id,
                )
                try:
                    result = self.execute_task(task)
                    logger.info(
                        "Task with id %s completed - Marking as completed",
                        task.id,
                    )
                    self._task_service.mark_task_completed(task.id, result)
                except KeyboardInterrupt as kb:
                    raise kb
                except Exception as e:
                    error_message = str(e)
                    logger.exception(
                        "Exception raised task with id %s completed - Marking as failed with error: %s",
                        task.id,
                        error_message,
                    )
                    self._task_service.mark_task_failed(task.id, error_message)

    def execute_task(self, task: ExtractionTask) -> ExtractionTaskResult:
        if task.type == ExtractionTaskType.EXTRACT_ACCOUNT:
            assert isinstance(task.task_config, ExtractAccountTaskConfig)
            return self._extractor.extract_account(task.task_config)
        elif task.type == ExtractionTaskType.EXTRACT_POST_LIST:
            assert isinstance(task.task_config, ExtractPostListTaskConfig)
            return self._extractor.extract_post_list(task.task_config)
        elif task.type == ExtractionTaskType.EXTRACT_POST_DETAILS:
            assert isinstance(task.task_config, ExtractPostDetailsTaskConfig)
            return self._extractor.extract_post_details(task.task_config)


def get_my_public_ip() -> str:
    response = requests.get("https://api4.my-ip.io/v2/ip.json")
    return response.json()["ip"]
