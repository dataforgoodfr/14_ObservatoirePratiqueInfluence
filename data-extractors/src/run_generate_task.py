import csv
from dataclasses import dataclass
import datetime
from urllib.parse import urlparse
import uuid
from extraction_task.extraction_task import (
    ExtractionTask,
    ExtractionTaskStatus,
    ExtractionTaskType,
)
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.local.task_repository import TaskRepository
from extraction_task.social_network import SocialNetwork


import logging


from typing import Literal


@dataclass
class GenerateTaskConfig:
    task_type: Literal["all", "account", "post-list"]
    published_after: datetime.datetime
    published_before: datetime.datetime
    replace: bool
    urls_file: str
    tasks_file: str


def run_generate_task(config: GenerateTaskConfig) -> None:
    logging.info("config: %s", config)

    generate_tasks_from_accounts(
        account_urls_file=config.urls_file,
        tasks_csv_file=config.tasks_file,
        task_type=config.task_type,
        published_after=config.published_after,
        published_before=config.published_before,
        replace=config.replace,
    )
    print(f"Successfully generated {config.tasks_file}")


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


def generate_tasks_from_accounts(
    account_urls_file: str,
    tasks_csv_file: str,
    task_type: Literal["all", "account", "post-list"],
    published_after: datetime.datetime,
    published_before: datetime.datetime,
    replace: bool,
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
