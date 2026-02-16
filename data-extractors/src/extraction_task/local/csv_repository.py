from collections.abc import Callable
import csv
from os import path
import os
from typing import Optional


class CsvRowRepository:
    """
    CSV based repository.
    WARNING: Not fit for production as it rewrites the whole file on every write
    """

    _csv_file: str
    _field_names: list[str]

    def __init__(self, csv_file: str, csv_field_names: list[str]):
        self._csv_file = csv_file
        self._field_names = list(csv_field_names)
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not path.exists(self._csv_file):
            os.makedirs(path.dirname(self._csv_file), exist_ok=True)
            with open(self._csv_file, "w") as f:
                w = csv.DictWriter(f, self._field_names)
                w.writeheader()

    def _find_row(self, row_predicate: Callable[[dict], bool]) -> Optional[dict]:
        rows = self._list_all_rows()
        for row in rows:
            if row_predicate(row.copy()):
                return row
        return None

    def _upsert_row(
        self, match_predicate: Callable[[dict], bool], update_value: dict
    ) -> dict:
        rows = self._list_all_rows()

        rowIndex: Optional[int] = next(
            (index for index, row in enumerate(rows) if match_predicate(row.copy())),
            None,
        )
        if rowIndex is None:
            self._append_rows([update_value])
            return update_value
        else:
            row = rows[rowIndex]
            for key in update_value:
                # patch provided values
                row[key] = update_value[key]
            self._replace_all_rows(rows)
            return row

    def _replace_all_rows(self, tasks: list[dict]) -> None:
        self._write_rows(tasks, replace=True)

    def _append_rows(self, rows: list[dict]) -> None:
        self._write_rows(rows, replace=False)

    def _list_all_rows(self) -> list[dict]:
        with open(self._csv_file) as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def _write_rows(self, rows: list[dict], replace: bool) -> None:
        with open(self._csv_file, "w" if replace else "a") as f:
            w = csv.DictWriter(f, self._field_names)
            if replace:
                w.writeheader()
            w.writerows(rows)
