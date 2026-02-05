#!/usr/bin/env python3
"""

This script reads account URLs from account_urls.csv and generates
a extraction_tasks.csv file with tasks for extracting account and post-list data.
"""

import csv
import datetime
import logging
from os import path
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
    if url.startswith("https://www.instagram.com/"):
        account_id = url.rstrip("/").split("/")[-1]
        return (SocialNetwork.INSTAGRAM, account_id)
    if url.startswith("https://www.youtube.com/channel/"):
        account_id = url.rstrip("/").split("/")[-1]
        return (SocialNetwork.YOUTUBE, account_id)
    if url.startswith("https://www.tiktok.com/"):
        account_id = url.rstrip("/").split("/")[-1]
        return (SocialNetwork.TIKTOK, account_id)
    else:
        raise Exception("unmatched url" + url)


published_after = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)
published_before = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)


def generate_tasks_from_accounts(account_urls_file: str, tasks_csv_file: str) -> None:
    # Read the input file
    with open(account_urls_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    urls = [row["Account Url"] for row in rows if row and row["Account Url"].strip()]

    # Prepare the output rows

    tasks: list[ExtractionTask] = []
    for url in urls:
        (social_network, account_id) = extract_network_and_account_id(url)

        # Generate two tasks per id: extract-account and extract-post-list

        account_task = ExtractionTask(
            id=uuid.uuid4(),
            social_network=social_network,
            type=ExtractionTaskType.EXTRACT_ACCOUNT,
            task_config=ExtractAccountTaskConfig(account_id=account_id),
            status=ExtractionTaskStatus.AVAILABLE,
            error=None,
            visible_at=None,
        )

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

        tasks.append(account_task)
        tasks.append(post_list_task)

    repo = TaskRepository(tasks_csv_file=tasks_csv_file)
    repo.replace_all(tasks)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    """Main function to execute the transformation."""
    data_folder = "data"
    input_file = path.join(data_folder, "account_urls.csv")
    output_file = path.join(data_folder, "extraction_tasks.csv")

    generate_tasks_from_accounts(input_file, output_file)
    print(f"Successfully generated {output_file}")


if __name__ == "__main__":
    main()
