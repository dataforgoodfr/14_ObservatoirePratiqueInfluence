"""Generic NocoDB client for upserting records."""

import logging
from typing import Any, TypedDict
from urllib.parse import quote

import requests

from app._config import settings

LOGGER = logging.getLogger(__name__)


class NocoRecord(TypedDict):
    """NocoDB record."""

    id: str
    fields: dict[str, Any]


class TableNotFoundError(Exception):
    """Exception raised when no table is found."""


class FieldNotFoundError(Exception):
    """Exception raised when no table is found."""


# TODO(iai): Merge this client with the one used in data-extractor
class NocoDBClient:
    """Generic NocoDB client for upserting records."""

    def __init__(self) -> None:
        """Initialize the NocoDB client.

        Args:
            config: NocoDB configuration

        """
        self._table_id_cache: dict[str, str] = {}
        self._base_url = f"{settings.nocodb_url}/api/v3"

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication.

        Returns:
            Dictionary of headers

        """
        return {
            "xc-token": settings.nocodb_api_token,
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        timeout: int = 10,
        **kwargs,
    ) -> dict[str, Any]:
        """Make an HTTP request to NocoDB API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint path
            timeout: The request timeout
            **kwargs: Additional arguments for requests

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails

        """
        url = f"{self._base_url}{endpoint}"
        headers = self._get_headers()

        try:
            response = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            LOGGER.exception("Nocodb Request failed {response.text}")
            raise

    def get_tables(self) -> list[dict[str, Any]]:
        """Get all tables in the base.

        Returns:
            List of table dictionaries

        """
        response = self._make_request(
            "GET",
            f"/meta/bases/{settings.nocodb_base_id}/tables",
        )
        return response.get("list", [])

    def update_record(
        self,
        table_id: str,
        record_id: str,
        record_data: dict[str, Any],
    ) -> NocoRecord:
        """Update an existing record.

        Args:
            table_id: Table ID
            record_id: Record ID
            record_data: Updated record data

        Returns:
            Updated record

        """
        endpoint = f"/data/{settings.nocodb_base_id}/{table_id}/records"
        payload = {"id": record_id, "fields": record_data}
        response = self._make_request("PATCH", endpoint, json=payload)
        records = response.get("records", [])
        return records[0]

    def create_record(self, table_id: str, record_data: dict[str, Any]) -> NocoRecord:
        """Create a new record.

        Args:
            table_id: Table ID
            record_data: Record data to create

        Returns:
            Created record

        """
        data = [{"fields": record_data}]
        response = self._make_request(
            "POST",
            f"/data/{settings.nocodb_base_id}/{table_id}/records",
            json=data,
        )
        records = response.get("records", [])
        return records[0]

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
        message = f"Table '{table_name}' not found in base"
        raise TableNotFoundError(message)

    def _find_record_id_by_logical_id(
        self,
        noco_table: str,
        logical_id: dict[str, Any],
    ) -> str | None:
        record = self._find_record_by_logical_id(noco_table, logical_id)
        return record["id"] if record else None

    def _find_record_by_logical_id(
        self,
        noco_table: str,
        logical_id: dict[str, Any],
    ) -> NocoRecord | None:
        table_id = self._get_table_id(noco_table)
        where = "~and".join([f"(\"{k}\", eq, '{quote(v)}')" for k, v in logical_id.items()])
        params: dict[str, Any] = {"where": where}

        response = self._make_request(
            "GET",
            f"/data/{settings.nocodb_base_id}/{table_id}/records",
            params=params,
        )
        records = response.get("records", [])
        if records:
            if len(records) > 1:
                LOGGER.warning("Duplicate record for logical_id: %s", logical_id)
            record_dict = records[0]
            return NocoRecord(id=record_dict["id"], fields=record_dict)
        return None

    def _get_table_fields(self, table_id: str) -> list[dict[str, Any]]:
        """Get all columns for a table.

        Args:
            table_id: Table ID

        Returns:
            List of fields

        """
        response = self._make_request(
            "GET", f"/meta/bases/{settings.nocodb_base_id}/tables/{table_id}"
        )
        return response.get("fields", [])

    def _get_link_field_id(self, table_id: str, field_name: str) -> str:
        columns = self._get_table_fields(table_id)
        for column in columns:
            if column.get("title") == field_name:
                return column["id"]

        message = f"Link field '{field_name}' not found in table"
        raise FieldNotFoundError(message)

    def link_record(
        self,
        from_table_id: str,
        link_field_id: str,
        from_record_id: str,
        target_record_id: str,
    ) -> None:
        """Link a record to another record via a link field.

        Args:
            from_table_id: Source table ID
            from_record_id: Source record ID
            link_field_id: Link field ID
            target_record_id: Target record ID to link to

        """
        data = {"id": target_record_id}
        endpoint = (
            f"/data/{settings.nocodb_base_id}/{from_table_id}/links/"
            f"{link_field_id}/{from_record_id}/"
        )
        self._make_request("POST", endpoint, json=data)

    def upsert_record(
        self,
        table_name: str,
        linked_field_mappings: dict[str, Any],
        logical_id: dict[str, Any],
        record: dict[str, Any],
    ) -> NocoRecord:
        """Upserts record into NOCODB."""
        table_id = self._get_table_id(table_name)

        existing_record_id = self._find_record_id_by_logical_id(
            table_name,
            logical_id,
        )

        if existing_record_id:
            result = self.update_record(table_id, existing_record_id, record)
            LOGGER.debug("Updated record %s with id %s", logical_id, result["id"])
        else:
            # Create new record
            result = self.create_record(table_id, record)
            LOGGER.debug("Created record %s with id %s", logical_id, result["id"])

        for field_name, mapping in linked_field_mappings.items():
            link_field_id = self._get_link_field_id(table_id, field_name)
            target_record_id = self._find_record_id_by_logical_id(
                mapping["target_table"], mapping["lookup"]
            )
            if target_record_id:
                self.link_record(
                    from_table_id=table_id,
                    link_field_id=link_field_id,
                    from_record_id=result["id"],
                    target_record_id=target_record_id,
                )

        return result
