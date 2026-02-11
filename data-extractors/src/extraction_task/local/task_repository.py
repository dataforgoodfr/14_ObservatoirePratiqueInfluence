from uuid import UUID
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskType,
)


import json
from typing import Callable, List, Optional

from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.local.csv_repository import CsvRowRepository
from extraction_task.social_network import SocialNetwork


class TaskRepository:
    _csv_repository: CsvRowRepository

    def __init__(self, tasks_csv_file: str):
        self._csv_repository = CsvRowRepository(
            tasks_csv_file, list(ExtractionTask.model_fields.keys())
        )

    def find_by_id(self, id: UUID) -> Optional[ExtractionTask]:
        row = self._csv_repository._find_row(self._make_by_id_predicate(id))

        return None if row is None else self._task_from_csv_row(row)

    def upsert(self, task: ExtractionTask) -> None:

        self._csv_repository._upsert_row(
            self._make_by_id_predicate(task.id), self._task_to_csv_row(task)
        )

    def get_first_acquirable_task(
        self, social_network: SocialNetwork
    ) -> Optional[ExtractionTask]:
        def acquirable_predicate(csv_row: dict) -> bool:
            t = self._task_from_csv_row(csv_row)
            return t.social_network == social_network and t.is_acquirable()

        row = self._csv_repository._find_row(acquirable_predicate)
        return None if row is None else self._task_from_csv_row(row)

    def replace_all(self, tasks: List[ExtractionTask]) -> None:
        self._csv_repository._replace_all_rows(
            [self._task_to_csv_row(t) for t in tasks]
        )

    def append_all(self, tasks: List[ExtractionTask]) -> None:
        self._csv_repository._append_rows([self._task_to_csv_row(t) for t in tasks])

    def list_all(self) -> List[ExtractionTask]:
        rows = self._csv_repository._list_all_rows()
        return [self._task_from_csv_row(r) for r in rows]

    def _task_from_csv_row(self, csv_row: dict) -> ExtractionTask:
        type: ExtractionTaskType = csv_row["type"]
        if type == ExtractionTaskType.EXTRACT_ACCOUNT:
            redict = ExtractAccountTaskConfig.model_validate_json(
                csv_row["task_config"]
            ).model_dump()
        elif type == ExtractionTaskType.EXTRACT_POST_LIST:
            redict = ExtractPostListTaskConfig.model_validate_json(
                csv_row["task_config"]
            ).model_dump()
        elif type == ExtractionTaskType.EXTRACT_POST_DETAILS:
            redict = ExtractPostDetailsTaskConfig.model_validate_json(
                csv_row["task_config"]
            ).model_dump()

        csv_row["task_config"] = redict

        if csv_row["visible_at"] == "":
            csv_row["visible_at"] = None

        return ExtractionTask.model_validate(csv_row)

    def _task_to_csv_row(self, task: ExtractionTask) -> dict:
        dict = task.model_dump()
        json_task_config = json.dumps(task.task_config.model_dump(mode="json"))
        dict["task_config"] = json_task_config
        return dict

    def _make_by_id_predicate(self, id: UUID) -> Callable[[dict], bool]:
        def match_by_id(csv_row: dict) -> bool:
            return self._task_from_csv_row(csv_row).id == id

        return match_by_id
