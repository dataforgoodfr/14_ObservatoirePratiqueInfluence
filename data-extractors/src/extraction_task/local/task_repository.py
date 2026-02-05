from uuid import UUID
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskType,
)


import csv
import json
import os
from os import path
from typing import Dict, List, Optional

from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.social_network import SocialNetwork


class TaskRepository:
    _csv_file: str

    def __init__(self, tasks_csv_file: str):
        self._csv_file = tasks_csv_file
        self._init_csv_file_if_missing()

    def _init_csv_file_if_missing(self) -> None:
        if not path.exists(self._csv_file):
            os.makedirs(path.dirname(self._csv_file), exist_ok=True)
            with open(self._csv_file, "w") as f:
                w = csv.DictWriter(f, ExtractionTask.__annotations__.keys())
                w.writeheader()

    def find_by_id(self, id: UUID) -> Optional[ExtractionTask]:
        tasks = self.list_all()
        return next((t for t in tasks if t.id == id), None)

    def upsert(self, task: ExtractionTask) -> None:
        tasks = self.list_all()

        taskIndex: Optional[int] = next(
            (i for i, a in enumerate(tasks) if a.id == task.id),
            None,
        )
        if taskIndex is None:
            tasks.append(task)
        else:
            tasks[taskIndex] = task

        self.replace_all(tasks)

    def get_first_acquirable_task(
        self, social_network: SocialNetwork
    ) -> Optional[ExtractionTask]:
        tasks = self.list_all()

        next_task: Optional[ExtractionTask] = next(
            (
                t
                for t in tasks
                if t.social_network == social_network and t.is_acquirable()
            ),
            None,
        )
        return next_task

    def replace_all(self, tasks: List[ExtractionTask]) -> None:
        with open(self._csv_file, "w") as f:
            w = csv.DictWriter(f, ExtractionTask.__annotations__.keys())
            w.writeheader()
            csv_rows = [self.__to_csv_dict(task) for task in tasks]
            w.writerows(csv_rows)

    def list_all(self) -> List[ExtractionTask]:
        with open(self._csv_file) as f:
            reader = csv.DictReader(f)
            rows_with_parsed_config = [self.__from_csv_dict(row) for row in reader]
            return [
                ExtractionTask.model_validate(row) for row in rows_with_parsed_config
            ]

    def __from_csv_dict(self, csv_row: Dict) -> ExtractionTask:
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

    def __to_csv_dict(self, task: ExtractionTask) -> Dict:
        dict = task.model_dump()
        json_task_config = json.dumps(task.task_config.model_dump(mode="json"))
        dict["task_config"] = json_task_config
        return dict
