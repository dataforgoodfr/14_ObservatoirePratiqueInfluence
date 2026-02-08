#!/usr/bin/env python3
"""

This script reads account URLs from account_urls.csv and generates
a extraction_tasks.csv file with tasks for extracting account and post-list data.
"""

import argparse
import csv
import datetime
import logging
from urllib.parse import urlparse
import uuid


from extraction_task.local.task_repository import TaskRepository
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskStatus,
    ExtractionTaskType,
)
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.social_network import SocialNetwork


def extract_network_and_account_id(url: str) -> tuple[SocialNetwork, str]:
    parsed = urlparse(url)
    netloc = parsed.netloc
    path_fragments = parsed.path.strip("/").split("/")
    if netloc == "www.instagram.com":
        account_id = path_fragments[-1]
        return (SocialNetwork.INSTAGRAM, account_id)
    if netloc == "www.youtube.com" and path_fragments[0] == "channel":
        account_id = path_fragments[-1]
        return (SocialNetwork.YOUTUBE, account_id)
    if netloc == "www.tiktok.com":
        account_id = path_fragments[-1]
        return (SocialNetwork.TIKTOK, account_id)
    else:
        raise Exception("unmatched url" + url)


# Default date range
DEFAULT_PUBLISHED_AFTER = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)
DEFAULT_PUBLISHED_BEFORE = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)


def generate_tasks_from_accounts(
    account_urls_file: str,
    tasks_csv_file: str,
    task_type: str = "all",
    published_after: datetime.datetime = DEFAULT_PUBLISHED_AFTER,
    published_before: datetime.datetime = DEFAULT_PUBLISHED_BEFORE,
    replace: bool = True,
) -> None:
    """
    Generate extraction tasks from account URLs.

    Args:
        account_urls_file: Path to the input CSV file with account URLs
        tasks_csv_file: Path to the output CSV file for extraction tasks
        task_type: Which task types to generate ("all", "account", or "post-list")
        published_after: Start date for post list extraction (ISO format or datetime)
        published_before: End date for post list extraction (ISO format or datetime)
        replace: If True, replace existing tasks; if False, append to existing tasks
    """
    # Read the input file
    with open(account_urls_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    urls = [row["Account Url"] for row in rows if row and row["Account Url"].strip()]

    # Prepare the output rows

    tasks: list[ExtractionTask] = []
    for url in urls:
        (social_network, account_id) = extract_network_and_account_id(url)

        # Generate tasks based on task_type parameter

        if task_type in ("all", "account"):
            account_task = ExtractionTask(
                id=uuid.uuid4(),
                social_network=social_network,
                type=ExtractionTaskType.EXTRACT_ACCOUNT,
                task_config=ExtractAccountTaskConfig(account_id=account_id),
                status=ExtractionTaskStatus.AVAILABLE,
                error=None,
                visible_at=None,
            )
            tasks.append(account_task)

        if task_type in ("all", "post-list"):
            post_list_task = ExtractionTask(
                id=uuid.uuid4(),
                social_network=social_network,
                type=ExtractionTaskType.EXTRACT_POST_LIST,
                task_config=ExtractPostListTaskConfig(
                    account_id=account_id,
                    published_after=published_after,
                    published_before=published_before,
                ),
                status=ExtractionTaskStatus.AVAILABLE,
                error=None,
                visible_at=None,
            )
            tasks.append(post_list_task)

    repo = TaskRepository(tasks_csv_file=tasks_csv_file)
    if replace:
        repo.replace_all(tasks)
    else:
        repo.append_all(tasks)


def parse_date(date_str: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(
        tzinfo=datetime.timezone.utc
    )


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    parser = argparse.ArgumentParser(
        description="Generate extraction tasks from account URLs."
    )
    parser.add_argument(
        "--task-type",
        choices=["all", "account", "post-list"],
        default="all",
        help="Which task types to generate (default: all)",
    )
    parser.add_argument(
        "--published-after",
        type=str,
        default="2025-01-01",
        help="Start date for post list extraction in YYYY-MM-DD  format (default: 2025-01-01)",
    )
    parser.add_argument(
        "--published-before",
        type=str,
        default="2026-01-01",
        help="End date for post list extraction in YYYY-MM-DD format (default: 2026-01-01)",
    )
    parser.add_argument(
        "--mode",
        choices=["replace", "append"],
        default="replace",
        help="Whether to replace existing tasks or append to them (default: replace)",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/account_urls.csv",
        help="Path to the input CSV file with account URLs (default: data/account_urls.csv)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/extraction_tasks.csv",
        help="Path to the output CSV file for extraction tasks (default: data/extraction_tasks.csv)",
    )

    args = parser.parse_args()

    # Parse dates
    published_after = parse_date(args.published_after)
    published_before = parse_date(args.published_before)

    # Determine if we should replace or append
    replace = args.mode == "replace"

    generate_tasks_from_accounts(
        account_urls_file=args.input,
        tasks_csv_file=args.output,
        task_type=args.task_type,
        published_after=published_after,
        published_before=published_before,
        replace=replace,
    )
    print(f"Successfully generated {args.output}")


if __name__ == "__main__":
    main()
