from dataclasses import dataclass
import os
from data_extractors.data_extractor import DataExtractor
from data_extractors.instagram.instagram_extractor import InstagramExtractor
from data_extractors.tiktok.tiktok_extractor import TiktokExtractor
from data_extractors.tiktok.tiktok_extractor_v2 import TiktokExtractorV2
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


import logging
from os import path


def create_extractor(social_network: SocialNetwork, cache_folder: str) -> DataExtractor:
    extractors = {
        SocialNetwork.INSTAGRAM: InstagramExtractor,
        SocialNetwork.TIKTOK: lambda: create_tiktok_extractor(cache_folder),
        SocialNetwork.YOUTUBE: lambda: create_youtube_extractor(cache_folder),
    }
    return extractors[social_network]()


def create_tiktok_extractor(cache_folder: str) -> DataExtractor:
    if os.getenv("TIKTOK_EXTRACTOR") == "V1":
        return TiktokExtractor()
    else:
        # Default to V2
        return TiktokExtractorV2(cache_folder=path.join(cache_folder, "tiktok"))


def create_youtube_extractor(cache_folder: str) -> YoutubeExtractor:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise Exception("YOUTUBE_API_KEY environment variable is required")
    api_config = YoutubeApiConfig(
        api_key=api_key,
        cache_config=DiskCacheConfig(cache_dir=path.join(cache_folder, "youtube")),
    )
    return YoutubeExtractor(api_config=api_config)


@dataclass
class ExtractConfig:
    social_network: SocialNetwork
    task_polling_interval: int
    tasks_file: str
    result_folder: str
    cache_folder: str


def run_extract(config: ExtractConfig) -> None:
    logging.info("config: %s", config)

    task_repository = TaskRepository(config.tasks_file)
    account_repository = AccountRepository(
        path.join(config.result_folder, "accounts.csv")
    )
    post_repository = PostRepository(path.join(config.result_folder, "posts.csv"))
    task_service: ExtractionTaskService = LocalExtractionTaskService(
        task_repository, account_repository, post_repository
    )

    extractor = create_extractor(
        config.social_network, cache_folder=config.cache_folder
    )

    loop = TaskProcessingLoop(
        social_network=config.social_network,
        task_repository=task_service,
        extractor=extractor,
        polling_interval=config.task_polling_interval,
    )

    loop.run()
