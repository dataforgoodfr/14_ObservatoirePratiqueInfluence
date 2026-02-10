from data_extractors.data_extractor import DataExtractor
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.extraction_task_result import (
    AccountExtractionResult,
    PostDetailsExtractionResult,
    PostListExtractionResult,
    PostListResultItem,
)

import datetime
import logging

from .youtube_api_client import Channel, YoutubeApiClient, post_url
from .youtube_api_config import YoutubeApiConfig

logger = logging.getLogger(__name__)


class YoutubeExtractor(DataExtractor):
    def __init__(self, api_config: YoutubeApiConfig) -> None:
        self.api_client = YoutubeApiClient(api_config)

    def extract_account(
        self, task_config: ExtractAccountTaskConfig
    ) -> AccountExtractionResult:
        try:
            logger.info(f"Extracting account for account_id: {task_config.account_id}")
            channel = self._channel_by_handle_or_id(task_config.account_id)
            logger.debug(
                f"Successfully fetched channel: {channel.title} (id: {channel.id})",
            )

            return AccountExtractionResult(
                data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                handle=channel.custom_url,
                description=channel.description,
                follower_count=channel.subscriber_count,
                following_count=0,  # YouTube doesn't have following concept
                post_count=channel.video_count,
                view_count=channel.view_count,
                like_count=0,  # No account-wide like count
                categories=channel.topic_categories,
            )
        except Exception as e:
            logger.error(f"Failed to extract account for {task_config.account_id}: {e}")
            raise Exception(f"Failed to extract account: {e}")

    def _channel_by_handle_or_id(self, handle_or_id: str) -> Channel:
        if handle_or_id.startswith("@"):
            logger.debug(f"Fetching channel by handle: {handle_or_id}")
            channel = self.api_client.get_channel_by_handle(handle_or_id)
        else:
            # assume id
            logger.debug(f"Fetching channel by id: {handle_or_id}")
            channel = self.api_client.get_channel_by_id(handle_or_id)
        return channel

    def extract_post_list(
        self, task_config: ExtractPostListTaskConfig
    ) -> PostListExtractionResult:
        try:
            logger.info(
                f"Extracting post list for account id: {task_config.account_id}, "
                f"published_after: {task_config.published_after}, "
                f"published_before: {task_config.published_before}",
            )
            channel = self._channel_by_handle_or_id(task_config.account_id)
            playlist_id = self.api_client.get_channel_uploads_playlist_id(channel.id)
            all_items = self.api_client.list_all_playlist_items(playlist_id)
            logger.debug(f"Fetched {len(all_items)} items from playlist")

            filtered_items = [
                item
                for item in all_items
                if task_config.published_after
                <= item.published_at
                <= task_config.published_before
            ]
            logger.debug(f"Filtered to {len(filtered_items)} items in date range")

            posts = [
                PostListResultItem(
                    post_id=item.video_id,
                    published_at=item.published_at,
                )
                for item in filtered_items
            ]

            logger.info(f"Returning {len(posts)} posts for {task_config.account_id}")
            return PostListExtractionResult(
                data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                posts=posts,
            )
        except Exception as e:
            logger.error(
                f"Failed to extract post list for {task_config.account_id}: {e}"
            )
            raise Exception(f"Failed to extract post list: {e}")

    def extract_post_details(
        self, task_config: ExtractPostDetailsTaskConfig
    ) -> PostDetailsExtractionResult:
        try:
            logger.info(f"Extracting post detail for video_id: {task_config.post_id}")
            video = self.api_client.get_video(task_config.post_id)
            logger.debug(f"Fetched video: {video.title}")

            return PostDetailsExtractionResult(
                data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                post_url=post_url(video.id, video.post_type),
                title=video.title,
                description=video.description,
                comment_count=int(video.comment_count) if video.comment_count else 0,
                view_count=video.view_count,
                like_count=int(video.like_count) if video.like_count else 0,
                repost_count=0,  # youtube does not have a repost concept
                share_count=0,  # youtube does not have a share concept
                tags=video.tags,
                categories=video.topic_categories,
                sn_has_paid_placement=video.has_paid_placement,
                sn_brand="",  # youtube does not provide brand info for product placement
                post_type="video",
                text_content="",  # not relevant for video posts
            )
        except Exception as e:
            logger.error(
                f"Failed to extract post detail for {task_config.post_id}: {e}"
            )
            raise Exception(f"Failed to extract post detail: {e}")
