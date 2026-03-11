import csv
import datetime
import logging
import uuid
from os import path
from typing import Literal, Optional, Self
from urllib.parse import urlparse

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from api_client import api_client
from api_client.api.default_api import DefaultApi
from default_api_backend_url import default_api_backend_url
from extraction_task.api.mappings import to_api_extractions_tasks
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


class GenerateTaskSettings(BaseSettings):
    """Settings for the generate-task command."""

    model_config = SettingsConfigDict(
        env_file=".env",
        nested_model_default_partial_update=True,
        env_nested_delimiter="__",
        extra="ignore",
    )
    task_type: Literal["all", "account", "post-list"] = Field(
        default="all", description="Which task types to generate"
    )
    published_after: datetime.datetime = Field(
        default=datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc),
        description="Start date for post list extraction in YYYY-MM-DD format",
    )
    published_before: datetime.datetime = Field(
        default=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc),
        description="End date for post list extraction in YYYY-MM-DD format",
    )

    urls_file: str = Field(
        default=path.join("data", "account_urls.csv"),
        description="Path to the input CSV file with account URLs",
    )

    backend: Literal["fs", "api"] = Field(
        default="api",
        description="Configure whether to use filesystem or server for tasks storage",
    )

    api_url: str = Field(
        default=default_api_backend_url,
        description="API backend url. Required when backend=api.",
    )

    api_key: Optional[str] = Field(
        default=None,
        description="API backend auth token. Required when backend=api.",
    )

    fs_replace: bool = Field(
        default=False,
        description="When using fs backend. Whether to replace existing tasks or append to them",
    )
    fs_tasks_file: str = Field(
        default=path.join("data", "extraction_tasks.csv"),
        description="FS backend tasks csv file",
    )

    @model_validator(mode="after")
    def check_required(self) -> Self:
        if self.backend == "api" and self.api_key is None:
            raise ValueError('api_key required when backend="api"')
        return self


def run_generate_task(config: GenerateTaskSettings) -> None:
    logging.info("config: %s", config)

    tasks = generate_tasks_from_accounts(
        account_urls_file=config.urls_file,
        task_type=config.task_type,
        published_after=config.published_after,
        published_before=config.published_before,
    )
    print(f"{len(tasks)} tasks generated.")

    if config.backend == "fs":
        print(f"Storing tasks to {config.fs_tasks_file} - replace: {config.fs_replace}")
        store_tasks_to_csv(tasks, config.fs_tasks_file, config.fs_replace)
    else:
        assert config.api_key is not None
        print(f"Storing tasks to api {config.api_url}")
        store_tasks_using_api(tasks, config.api_url, config.api_key)


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
        account_id = path_fragments[-1].strip("@")  # Remove leading @
        return (SocialNetwork.TIKTOK, account_id)
    else:
        raise Exception("unmatched url" + url)


def generate_tasks_from_accounts(
    account_urls_file: str,
    task_type: Literal["all", "account", "post-list"],
    published_after: datetime.datetime,
    published_before: datetime.datetime,
) -> list[ExtractionTask]:
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

    return tasks


def store_tasks_to_csv(
    tasks: list[ExtractionTask], tasks_csv_file: str, replace: bool
) -> None:
    repo = TaskRepository(tasks_csv_file=tasks_csv_file)
    if replace:
        repo.replace_all(tasks)
    else:
        repo.append_all(tasks)


def store_tasks_using_api(
    tasks: list[ExtractionTask], api_url: str, api_token: str
) -> None:
    configuration = api_client.Configuration(access_token=api_token, host=api_url)
    client = api_client.ApiClient(configuration=configuration)
    api = DefaultApi(client)
    api.register_tasks_extraction_task_post(to_api_extractions_tasks(tasks))
