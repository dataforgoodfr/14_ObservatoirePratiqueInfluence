import logging
import os
from os import path
from typing import Literal, Optional, Self

from pydantic import AliasChoices, BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from default_api_backend_url import default_api_backend_url
from extraction_task.api.api_extraction_task_service import ApiExtractionTaskService
from data_extractors.data_extractor import DataExtractor
from data_extractors.instagram.instagram_extractor import InstagramExtractor
from data_extractors.tiktok.tiktok_extractor import TiktokExtractor
from data_extractors.tiktok.tiktok_extractor_v2 import TiktokExtractorV2
from data_extractors.tiktok.tiktokapi import TikTokApiConfig
from data_extractors.youtube.disk_cache import DiskCacheConfig
from data_extractors.youtube.youtube_api_config import YoutubeApiConfig
from data_extractors.youtube.youtube_extractor import YoutubeExtractor
from extraction_task.extraction_task_service import ExtractionTaskService
from extraction_task.local.account_repository import AccountRepository
from extraction_task.local.local_extraction_task_service import (
    LocalExtractionTaskService,
)
from extraction_task.local.post_repository import PostRepository
from extraction_task.local.task_repository import TaskRepository
from extraction_task.social_network import SocialNetwork
from task_processing_loop import TaskProcessingLoop


class YoutubeSettings(BaseModel):
    api_key: Optional[str] = Field(
        default=None, description="youtube api key. Required for youtube extractor."
    )


class TiktokSettings(BaseModel):
    implementation: Literal["V1", "V2"] = Field(
        default="V2", description="Extractor version to use"
    )

    ms_token: Optional[str] | Literal["PLAYWRIGHT"] = Field(
        default="PLAYWRIGHT", description="Extractor v2: how to get ms_token"
    )
    headless: bool = Field(
        default=False, description="Extractor v2: whether to use headless mode."
    )


class ExtractSettings(BaseSettings):
    """Settings for the extract command."""

    model_config = SettingsConfigDict(
        env_file=".env",
        nested_model_default_partial_update=True,
        env_nested_delimiter="__",
        extra="ignore",
    )

    social_network: SocialNetwork = Field(
        validation_alias=AliasChoices("n", "social_network"),
        default=SocialNetwork.YOUTUBE,
        description="Social Network",
    )
    task_polling_interval: int = Field(
        default=10, ge=1, description="Task polling interval seconds"
    )
    cache_folder: str = Field(
        default=path.join("data", ".cache"), description="Cache folder"
    )
    cache_ttl_seconds: int = Field(
        default=3600 * 24 * 7, description="Cache time to live in seconds"
    )

    exit_after_task_failure: bool | int = Field(
        default=True,
        description="Configure if exti after task failure: True|False or number of failure before exit",
    )

    backend: Literal["fs", "api"] = Field(
        default="api",
        description="Configure whether to use filesystem or server to acquire tasks and store results",
    )

    api_url: str = Field(
        default=default_api_backend_url,
        description="API backend url. Required when backend=api.",
    )

    api_key: Optional[str] = Field(
        default=None,
        description="API backend auth token. Required when backend=api.",
    )
    fs_tasks_file: str = Field(
        default=path.join("data", "extraction_tasks.csv"),
        description="FS backend tasks csv file",
    )
    fs_result_folder: str = Field(
        default=path.join("data", "results"), description="FS backend Result folder"
    )

    youtube: YoutubeSettings = Field(
        default=YoutubeSettings(), description="Youtube extractor settings"
    )
    tiktok: TiktokSettings = Field(
        default=TiktokSettings(), description="Tiktok extractor settings"
    )

    @model_validator(mode="after")
    def check_required(self) -> Self:
        if self.backend == "api" and self.api_key is None:
            raise ValueError('api_key required when backend="api"')

        if self.social_network == "youtube" and self.youtube.api_key is None:
            raise ValueError('youtube.api_key required when social-network="youtube"')
        return self


def run_extract(config: ExtractSettings) -> None:
    logging.info("config: %s", config)

    task_service = create_task_service(config)

    extractor = create_extractor(config)

    loop = TaskProcessingLoop(
        social_network=config.social_network,
        task_repository=task_service,
        extractor=extractor,
        polling_interval=config.task_polling_interval,
        exit_after_tasks_failure=config.exit_after_task_failure,
    )

    loop.run()


def create_task_service(config: ExtractSettings) -> ExtractionTaskService:
    if config.backend == "api":
        assert config.api_key is not None
        return ApiExtractionTaskService(config.api_url, config.api_key)
    else:
        task_repository = TaskRepository(config.fs_tasks_file)
        account_repository = AccountRepository(
            path.join(config.fs_result_folder, "accounts.csv")
        )
        post_repository = PostRepository(
            path.join(config.fs_result_folder, "posts.csv")
        )
        return LocalExtractionTaskService(
            task_repository, account_repository, post_repository
        )


def create_extractor(config: ExtractSettings) -> DataExtractor:
    extractors = {
        SocialNetwork.INSTAGRAM: lambda: create_instagram_extractor(
            config.cache_folder, config.cache_ttl_seconds
        ),
        SocialNetwork.TIKTOK: lambda: create_tiktok_extractor(
            config.cache_folder, config.cache_ttl_seconds, config.tiktok
        ),
        SocialNetwork.YOUTUBE: lambda: create_youtube_extractor(
            config.cache_folder, config.cache_ttl_seconds, config.youtube
        ),
    }
    return extractors[config.social_network]()


def create_tiktok_extractor(
    cache_folder: str, cache_ttl_seconds: int, settings: TiktokSettings
) -> DataExtractor:
    if os.getenv("TIKTOK_EXTRACTOR") == "V1":
        return TiktokExtractor()
    else:
        # Default to V2
        return TiktokExtractorV2(
            cache_folder=path.join(cache_folder, "tiktok"),
            cache_ttl_seconds=cache_ttl_seconds,
            api_config=TikTokApiConfig(
                headless=settings.headless, ms_token=settings.ms_token
            ),
        )


def create_instagram_extractor(
    cache_folder: str, cache_ttl_seconds: int
) -> DataExtractor:
    return InstagramExtractor(
        cache_folder=path.join(cache_folder, "instagram"),
        cache_ttl_seconds=cache_ttl_seconds,
    )


def create_youtube_extractor(
    cache_folder: str, cache_ttl_seconds: int, youtube_settings: YoutubeSettings
) -> YoutubeExtractor:
    assert youtube_settings.api_key is not None
    api_config = YoutubeApiConfig(
        api_key=youtube_settings.api_key,
        cache_config=DiskCacheConfig(
            cache_dir=path.join(cache_folder, "youtube"),
            ttl_seconds=cache_ttl_seconds,
        ),
    )
    return YoutubeExtractor(api_config=api_config)
