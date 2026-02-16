"""Generic NocoDB client for upserting records from CSV files."""

import csv
import logging
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypedDict

import requests

from get_required_env import get_required_env


@dataclass
class NocoDBConfig:
    """Configuration for NocoDB connection."""

    url: str
    base_id: str
    api_token: str

    @classmethod
    def from_env(cls) -> "NocoDBConfig":
        return NocoDBConfig(
            url=get_required_env("NOCODB_URL"),
            base_id=get_required_env("NOCODB_BASE_ID"),
            api_token=get_required_env("NOCODB_API_TOKEN"),
        )


@dataclass
class FieldMapping:
    pass


@dataclass
class CsvValueFieldMapping(FieldMapping):
    csv_field: str
    transform: Optional[Callable[[Any], Any]] = None


@dataclass
class LinkedIdFieldMapping(FieldMapping):
    target_table: str
    lookup: dict[str, CsvValueFieldMapping]  # Link Target  field -> Csv Value lookup


class NocoRecord(TypedDict):
    id: str
    fields: dict[str, Any]


logger = logging.getLogger(__name__)


@dataclass
class TableConfig:
    """Configuration for a NocoDB table."""

    table_name: str
    data_field_mappings: dict[
        str, CsvValueFieldMapping
    ]  # noco_field_name -> FieldMapping
    logical_id_fields: list[str]  # noco fields that should be used for upsert
    linked_field_mappings: dict[
        str, LinkedIdFieldMapping
    ]  # link_field_name -> FieldMapping


class NocoDBClient:
    """Generic NocoDB client for upserting records."""

    def __init__(self, config: NocoDBConfig) -> None:
        """Initialize the NocoDB client.

        Args:
            config: NocoDB configuration
        """
        self.config = config
        self._table_id_cache: dict[str, str] = {}
        self._base_url = f"{config.url.rstrip('/')}/api/v3"

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication.

        Returns:
            Dictionary of headers
        """
        return {
            "xc-token": self.config.api_token,
            "Content-Type": "application/json",
        }

    def _make_request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Make an HTTP request to NocoDB API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails
        """
        url = f"{self._base_url}{endpoint}"
        headers = self._get_headers()

        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def get_tables(self) -> list[dict[str, Any]]:
        """Get all tables in the base.

        Returns:
            List of table dictionaries
        """
        response = self._make_request(
            "GET", f"/meta/bases/{self.config.base_id}/tables"
        )
        return response.get("list", [])

    def update_record(
        self, table_id: str, record_id: str, record_data: dict[str, Any]
    ) -> NocoRecord:
        """Update an existing record.

        Args:
            table_id: Table ID
            record_id: Record ID
            data: Updated record data

        Returns:
            Updated record
        """
        endpoint = f"/data/{self.config.base_id}/{table_id}/records"
        payload = {"id": record_id, "fields": record_data}
        response = self._make_request("PATCH", endpoint, json=payload)
        records = response.get("records", [])
        return records[0]

    def create_record(self, table_id: str, record_data: dict[str, Any]) -> NocoRecord:
        """Create a new record.

        Args:
            table_id: Table ID
            data: Record data to create

        Returns:
            Created record
        """
        data = [{"fields": record_data}]
        response = self._make_request(
            "POST", f"/data/{self.config.base_id}/{table_id}/records", json=data
        )
        records = response.get("records", [])
        return records[0]

    def upsert_from_csv(
        self,
        table_config: TableConfig,
        csv_path: str,
    ) -> list[NocoRecord]:
        """Upsert records from a CSV file to NocoDB.

        Args:
            table_config: Table configuration
            csv_path: Path to CSV file
            lookup_cache: Cache for resolving links

        Returns:
            List of upserted records
        """
        if not os.path.exists(csv_path):
            raise Exception(f"CSV file not found: {csv_path}")

        results: list[NocoRecord] = []

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            row_count = len(rows)
            for i, row in enumerate(rows):
                try:
                    logger.info(
                        "Upserting record %s / %s from csv %s",
                        i + 1,
                        row_count,
                        csv_path,
                    )
                    result = self.upsert_record(table_config, row)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to upsert record: {e}")
                    logger.error(f"Record data: {row}")
                    raise

        return results

    def upsert_record(
        self, table_config: TableConfig, csv_record: dict[str, Any]
    ) -> NocoRecord:
        table_id = self._get_table_id(table_config.table_name)

        # Map fields
        mapped_record = self._map_fields(csv_record, table_config.data_field_mappings)

        # Build logical ID for lookup
        logical_id = {
            k: v
            for k, v in mapped_record.items()
            if k in table_config.logical_id_fields
        }

        existing_record_id = self._find_record_id_by_logical_id(
            table_config.table_name, logical_id
        )

        if existing_record_id:
            result = self.update_record(table_id, existing_record_id, mapped_record)
            logger.debug(f"Updated record {logical_id} with id {result['id']}")
        else:
            # Create new record
            result = self.create_record(table_id, mapped_record)
            logger.debug(f"Created record {logical_id} with id {result['id']}")

        for field_name, mapping in table_config.linked_field_mappings.items():
            link_field_id = self._get_link_field_id(table_id, field_name)
            target_record_id = self._resolved_target_record_id(csv_record, mapping)
            if target_record_id:
                self.link_record(
                    from_table_id=table_id,
                    link_field_id=link_field_id,
                    from_record_id=result["id"],
                    target_record_id=target_record_id,
                )

        return result

    def _get_table_id(self, table_name: str) -> str:
        """Get table ID by table name.

        Args:
            table_name: Name of the table

        Returns:
            Table ID

        Raises:
            Exception: If table not found
        """
        if table_name in self._table_id_cache:
            return self._table_id_cache[table_name]

        tables = self.get_tables()
        for table in tables:
            if table.get("title") == table_name:
                table_id = table["id"]
                self._table_id_cache[table_name] = table_id
                return table_id

        raise Exception(f"Table '{table_name}' not found in base")

    def _map_fields(
        self, csv_record: dict[str, Any], mappings: dict[str, CsvValueFieldMapping]
    ) -> dict[str, Any]:
        """Map CSV fields to NocoDB fields.

        Args:
            csv_record: CSV record data
            mappings: Field mappings (noco_field_name -> FieldMapping)

        Returns:
            Mapped record data
        """
        mapped: dict[str, Any] = {}
        for target_table_noco_field, mapping in mappings.items():
            if isinstance(mapping, CsvValueFieldMapping):
                value = self._map_value(csv_record, mapping)
                mapped[target_table_noco_field] = value
            elif isinstance(mapping, LinkedIdFieldMapping):
                target_logical_id: dict[str, Any] = {}
                for target_table_noco_field, lookup_mapping in mapping.lookup.items():
                    value = self._map_value(csv_record, lookup_mapping)
                    if lookup_mapping.transform is not None and value is not None:
                        value = lookup_mapping.transform(value)
                    target_logical_id[target_table_noco_field] = value
                self._find_record_by_logical_id(mapping.target_table, target_logical_id)

                # TODO lookup target table record with where clause
                # Link fields are resolved separately
                pass
        return mapped

    def _resolved_target_record_id(
        self, csv_record: dict[str, Any], linked_id_mapping: LinkedIdFieldMapping
    ) -> str | None:
        target_logical_id: dict[str, Any] = {}
        for target_table_noco_field, lookup_mapping in linked_id_mapping.lookup.items():
            value = self._map_value(csv_record, lookup_mapping)
            if lookup_mapping.transform is not None and value is not None:
                value = lookup_mapping.transform(value)
            target_logical_id[target_table_noco_field] = value
        return self._find_record_id_by_logical_id(
            linked_id_mapping.target_table, target_logical_id
        )

    def _find_record_id_by_logical_id(
        self, noco_table: str, logical_id: dict[str, Any]
    ) -> str | None:
        # TODO implement in memory caching
        record = self._find_record_by_logical_id(noco_table, logical_id)
        return record["id"] if record else None

    def _find_record_by_logical_id(
        self, noco_table: str, logical_id: dict[str, Any]
    ) -> NocoRecord | None:
        table_id = self._get_table_id(noco_table)
        where = "~and".join([f"(\"{k}\", eq, '{v}')" for k, v in logical_id.items()])
        params: dict[str, Any] = {"where": where}

        response = self._make_request(
            "GET", f"/data/{self.config.base_id}/{table_id}/records", params=params
        )
        records = response.get("records", [])
        if records:
            if len(records) > 1:
                logger.warning(f"Duplicate record for logical_id: {logical_id}")
            record_dict = records[0]
            return NocoRecord(id=record_dict["id"], fields=record_dict)
        else:
            return None

    def _map_value(
        self, csv_record: dict[str, Any], mapping: CsvValueFieldMapping
    ) -> Any:
        value = csv_record.get(mapping.csv_field)
        if mapping.transform is not None and value is not None:
            value = mapping.transform(value)
        return value

    def _get_table_fields(self, table_id: str) -> list[dict[str, Any]]:
        """Get all columns for a table.

        Args:
            table_id: Table ID

        Returns:
            List of fields
        """
        response = self._make_request(
            "GET", f"/meta/bases/{self.config.base_id}/tables/{table_id}"
        )
        return response.get("fields", [])

    def _get_link_field_id(self, table_id: str, field_name: str) -> str:
        columns = self._get_table_fields(table_id)
        for column in columns:
            if column.get("title") == field_name:
                return column["id"]

        raise Exception(f"Link field '{field_name}' not found in table")

    def link_record(
        self,
        from_table_id: str,
        link_field_id: str,
        from_record_id: str,
        target_record_id: str,
    ) -> None:
        """Link a record to another record via a link field.

        Args:
            record_id: Source record ID
            link_field_id: Link field ID
            target_record_id: Target record ID to link to
        """
        data = {"id": target_record_id}
        endpoint = f"/data/{self.config.base_id}/{from_table_id}/links/{link_field_id}/{from_record_id}/"
        self._make_request("POST", endpoint, json=data)
