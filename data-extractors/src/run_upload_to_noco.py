"""Upload results from CSV files to NocoDB."""

import logging
from dataclasses import dataclass
from os import path

from get_required_env import get_required_env
from nocodb_client import (
    CsvValueFieldMapping,
    LinkedIdFieldMapping,
    NocoDBClient,
    NocoDBConfig,
    TableConfig,
)


def parse_commma_separated_list(value: str) -> list[str]:
    if not value or value.strip() == "":
        return []
    return value.split(",")


def parse_bool(value: str) -> bool:
    """Parse boolean field from CSV.

    Args:
        value: Boolean string

    Returns:
        Boolean value
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes")
    return bool(value)


# Table configurations
def account_table_config(account_table_name: str) -> TableConfig:
    return TableConfig(
        table_name=account_table_name,
        data_field_mappings={
            "Social Network": CsvValueFieldMapping("social_network"),
            "Account Id": CsvValueFieldMapping("account_id"),
            "Account Extraction Date": CsvValueFieldMapping("account_extraction_date"),
            "Handle": CsvValueFieldMapping("handle"),
            "Description": CsvValueFieldMapping("description"),
            "Follower Count": CsvValueFieldMapping("follower_count"),
            "Following Count": CsvValueFieldMapping("following_count"),
            "Post Count": CsvValueFieldMapping("post_count"),
            "View Count": CsvValueFieldMapping("view_count"),
            "Like Count": CsvValueFieldMapping("like_count"),
            "Categories": CsvValueFieldMapping("categories"),
        },
        linked_field_mappings={},
        logical_id_fields=["Social Network", "Account Id"],
    )


def post_table_config(post_table_name: str, account_table_name: str) -> TableConfig:
    return TableConfig(
        table_name=post_table_name,
        data_field_mappings={
            "Social Network": CsvValueFieldMapping("social_network"),
            "Post Id": CsvValueFieldMapping("post_id"),
            # "PostExtractionDate": CsvValueFieldMapping("post_extraction_date"),
            "Post Url": CsvValueFieldMapping("post_url"),
            "Title": CsvValueFieldMapping("title"),
            "Description": CsvValueFieldMapping("description"),
            "Comment Count": CsvValueFieldMapping("comment_count"),
            "View Count": CsvValueFieldMapping("view_count"),
            "Repost Count": CsvValueFieldMapping("repost_count"),
            "Like Count": CsvValueFieldMapping("like_count"),
            "Share Count": CsvValueFieldMapping("share_count"),
            "Categories": CsvValueFieldMapping("categories"),
            "Tags": CsvValueFieldMapping("tags"),
            "SN Has Paid Placement": CsvValueFieldMapping(
                "sn_has_paid_placement", transform=parse_bool
            ),
            "SN Brand": CsvValueFieldMapping("sn_brand"),
            "Post Type": CsvValueFieldMapping("post_type"),
            # "TextContent": CsvValueFieldMapping("text_content"),
        },
        logical_id_fields=["Post Id"],
        linked_field_mappings={
            "Account": LinkedIdFieldMapping(
                target_table=account_table_name,
                lookup={
                    "Social Network": CsvValueFieldMapping("social_network"),
                    "Account Id": CsvValueFieldMapping("account_id"),
                },
            ),
        },
    )


@dataclass
class UploadToNocoConfig:
    """Configuration for uploading to NocoDB."""

    result_folder: str = path.join("data", "results")
    accounts_csv: str = path.join("data", "results", "accounts.csv")
    posts_csv: str = path.join("data", "results", "posts.csv")


def run_upload_to_noco(config: UploadToNocoConfig) -> None:
    """Upload accounts and posts from CSV to NocoDB.

    Args:
        config: Upload configuration

    Raises:
        Exception: If NOCODB_API_TOKEN is not set or files don't exist
    """
    logging.info("config: %s", config)

    # Initialize NocoDB client
    noco_config = NocoDBConfig.from_env()
    client = NocoDBClient(noco_config)

    account_table_name = get_required_env("NOCODB_ACCOUNT_TABLE_NAME")
    post_table_name = get_required_env("NOCODB_POST_TABLE_NAME")
    # Upload accounts first (no dependencies)
    logging.info("Uploading accounts from %s...", config.accounts_csv)
    accounts = client.upsert_from_csv(
        account_table_config(account_table_name),
        config.accounts_csv,
    )
    logging.info("Uploaded %d accounts", len(accounts))

    # Upload posts (depends on accounts)
    logging.info("Uploading posts from %s...", config.posts_csv)
    posts = client.upsert_from_csv(
        post_table_config(post_table_name, account_table_name), config.posts_csv
    )
    logging.info("Uploaded %d posts", len(posts))

    logging.info("Upload completed successfully!")
