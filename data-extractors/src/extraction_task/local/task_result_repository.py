import os
from os import path
from pathlib import Path
from uuid import UUID

from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.extraction_task_result import (
    AccountExtractionResult,
    PostDetailsExtractionResult,
    PostListExtractionResult,
)


class TaskResultRepository:
    _accounts_folder: str
    _post_list_folder: str
    _post_details_folder: str

    def __init__(self, results_folder: str):
        self._accounts_folder = path.join(results_folder, "accounts")
        self._post_list_folder = path.join(results_folder, "post_list")
        self._post_details_folder = path.join(results_folder, "post_details")
        os.makedirs(self._accounts_folder, exist_ok=True)
        os.makedirs(self._post_list_folder, exist_ok=True)
        os.makedirs(self._post_details_folder, exist_ok=True)

    def persist_extract_post_details_result(
        self,
        task_id: UUID,
        task_result: PostDetailsExtractionResult,
        task_config: ExtractPostDetailsTaskConfig,
    ) -> None:
        Path(
            path.join(
                self._post_details_folder,
                f"task-{task_id}-post-{task_config.post_id}.json",
            )
        ).write_text(task_result.model_dump_json(indent=2))

    def persist_extract_post_list_result(
        self,
        task_id: UUID,
        task_result: PostListExtractionResult,
        task_config: ExtractPostListTaskConfig,
    ) -> None:
        Path(
            path.join(
                self._post_list_folder,
                f"task-{task_id}-channel-{task_config.account_id}.json",
            )
        ).write_text(task_result.model_dump_json(indent=2))

    def persist_extract_account_result(
        self,
        task_id: UUID,
        task_result: AccountExtractionResult,
        task_config: ExtractAccountTaskConfig,
    ) -> None:
        Path(
            path.join(
                self._accounts_folder,
                f"task-{task_id}-channel-{task_config.account_id}.json",
            )
        ).write_text(task_result.model_dump_json(indent=2))
