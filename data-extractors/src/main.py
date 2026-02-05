import argparse
from dataclasses import dataclass
import logging
import logging.config
from os import path
import os
from data_extractors.instagram.instagram_extractor import InstagramExtractor
from data_extractors.tiktok.tiktok_extractor import TiktokExtractor
from data_extractors.youtube.disk_cache import DiskCacheConfig
from data_extractors.youtube.youtube_api_config import YoutubeApiConfig
from data_extractors.youtube.youtube_extractor import YoutubeExtractor
from extraction_task.local.local_extraction_task_service import (
    LocalExtractionTaskService,
)
from extraction_task.local.task_repository import TaskRepository
from extraction_task.local.task_result_repository import (
    TaskResultRepository,
)
from task_processing_loop import TaskProcessingLoop

from data_extractors.data_extractor import DataExtractor
from extraction_task.extraction_task_service import (
    ExtractionTaskService,
)
from extraction_task.social_network import SocialNetwork


def create_extractor(social_network: SocialNetwork, cache_folder: str) -> DataExtractor:
    match social_network:
        case SocialNetwork.INSTAGRAM:
            return InstagramExtractor()
        case SocialNetwork.TIKTOK:
            return TiktokExtractor()
        case SocialNetwork.YOUTUBE:
            api_key = os.getenv("YOUTUBE_API_KEY")
            if not api_key:
                raise Exception("YOUTUBE_API_KEY environment variable is required")
            api_config = YoutubeApiConfig(
                api_key=api_key,
                cache_config=DiskCacheConfig(
                    cache_dir=path.join(cache_folder, "youtube")
                ),
            )
            return YoutubeExtractor(api_config=api_config)


@dataclass
class Config:
    social_network: SocialNetwork
    task_polling_interval: int
    task_file: str
    result_folder: str
    cache_folder: str


def parse_arguments() -> Config:
    parser = argparse.ArgumentParser(
        prog="data_extractors",
    )

    parser.add_argument(
        "-n",
        "--social-network",
        help="Social Network",
        type=SocialNetwork,
        dest="social_network",
        choices=list(SocialNetwork),
        default=SocialNetwork.YOUTUBE,
    )

    parser.add_argument(
        "-p",
        "--polling-interval",
        dest="task_polling_interval",
        help="Task polling interval seconds",
        type=int,
        default=10,
    )

    parser.add_argument(
        "-i",
        "--task-file",
        dest="task_file",
        help="Task csv file",
        default=path.join("data", "extraction_tasks.csv"),
    )
    parser.add_argument(
        "-o",
        "--result-folder",
        dest="result_folder",
        help="Result folder",
        default=path.join("data", "results"),
    )

    parser.add_argument(
        "-c",
        "--cache-folder",
        dest="cache_folder",
        help="Cache folder",
        default=path.join("data", ".cache"),
    )

    result = parser.parse_args()

    return Config(
        social_network=result.social_network,
        task_polling_interval=result.task_polling_interval,
        task_file=result.task_file,
        result_folder=result.result_folder,
        cache_folder=result.cache_folder,
    )


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    config = parse_arguments()

    logging.info("config: %s", config)

    task_repository = TaskRepository(config.task_file)
    result_repository = TaskResultRepository(config.result_folder)
    task_service: ExtractionTaskService = LocalExtractionTaskService(
        task_repository, result_repository
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


if __name__ == "__main__":
    main()
