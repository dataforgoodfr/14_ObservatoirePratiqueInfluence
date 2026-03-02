import asyncio
import datetime
import json
import logging
from os import path
from pathlib import Path

from TikTokApi import TikTokApi
import diskcache

from data_extractors.data_extractor import DataExtractor
from data_extractors.tiktok.tiktokapi import (
    create_sessions,
    get_videos_for_date_range,
)
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

logger = logging.getLogger(__name__)


class TiktokExtractorV2(DataExtractor):
    def __init__(self, cache_folder: str, write_raw_data_to_disk: bool = False) -> None:
        self.cache = diskcache.Cache(
            directory=cache_folder,
        )
        # 7 days expiry
        self.cache_expire_seconds = 3600 * 24 * 7
        # Whether to store raw API data for further analysis/reuse
        self.write_raw_data = write_raw_data_to_disk
        if write_raw_data_to_disk:
            self.raw_data_folder = Path(path.join(cache_folder, "raw_data"))
            self.raw_data_folder.mkdir(parents=True, exist_ok=True)

    def extract_account(
        self,
        task_config: ExtractAccountTaskConfig,
    ) -> AccountExtractionResult:
        return asyncio.run(self._extract_account_async(task_config))

    async def _extract_account_async(
        self,
        task_config: ExtractAccountTaskConfig,
    ) -> AccountExtractionResult:
        async with TikTokApi() as api:
            await create_sessions(api)
            user_data = await api.user(username=task_config.account_id).info()
            self._write_user_dict_to_disk(task_config.account_id, user_data)

            user_info = user_data["userInfo"]
            user_info_user = user_info["user"]
            user_info_statsV2 = user_info["statsV2"]
            return AccountExtractionResult(
                data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                handle=user_info_user["uniqueId"],
                description=user_info_user["signature"],
                follower_count=int(user_info_statsV2["followerCount"]),
                following_count=int(user_info_statsV2["followingCount"]),
                post_count=int(user_info_statsV2["videoCount"]),
                like_count=int(user_info_statsV2["heartCount"]),
                view_count=0,  # not availabled at user level
                categories=[],  # not availabled
            )

    def extract_post_list(
        self, task_config: ExtractPostListTaskConfig
    ) -> PostListExtractionResult:
        """Extract list of posts from a TikTok account within a date range.

        Uses TikTokApi to fetch user videos and filters by published_after/published_before.
        """
        return asyncio.run(self._extract_post_list_async(task_config))

    async def _extract_post_list_async(
        self, task_config: ExtractPostListTaskConfig
    ) -> PostListExtractionResult:
        logger.info(
            f"Extracting post list for account_id: {task_config.account_id}, "
            f"published_after: {task_config.published_after}, "
            f"published_before: {task_config.published_before}"
        )

        posts: list[PostListResultItem] = []

        try:
            async with TikTokApi() as api:
                await create_sessions(api)

                user = api.user(username=task_config.account_id)
                videos = await get_videos_for_date_range(
                    user,
                    # video dates are unaware of tzinfo
                    task_config.published_after.replace(tzinfo=None),
                    task_config.published_before.replace(tzinfo=None),
                )

                # Store post_result details in cache to avoid refetching
                # when extract_post_details is called during cache duration
                for video in videos:
                    self._write_video_dict_to_disk(video.id, video.as_dict)
                    post_details_result = self._build_post_details_result_from_video(
                        video.as_dict
                    )
                    self.cache.set(
                        self._video_cache_key(video.id),
                        post_details_result,
                        expire=self.cache_expire_seconds,
                    )

                posts = [
                    PostListResultItem(
                        post_id=v.id,
                        published_at=v.create_time.replace(
                            tzinfo=datetime.timezone.utc
                        ),
                    )
                    for v in videos
                ]

                logger.info(
                    f"Found {len(posts)} posts for {task_config.account_id} in date range"
                )

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
        self,
        task_config: ExtractPostDetailsTaskConfig,
    ) -> PostDetailsExtractionResult:
        return asyncio.run(self._extract_post_details_async(task_config))

    async def _extract_post_details_async(
        self,
        task_config: ExtractPostDetailsTaskConfig,
    ) -> PostDetailsExtractionResult:
        video_id = task_config.post_id
        cache_key = self._video_cache_key(task_config.post_id)
        cached_value = self.cache.get(cache_key)
        if cached_value:
            logger.info(f"CACHED_POST found for: {video_id}")
            return cached_value

        async with TikTokApi() as api:
            await create_sessions(api)
            user_agnostic_video_url = f"https://www.tiktok.com/@tiktok/video/{video_id}"
            video_data = await api.video(url=user_agnostic_video_url).info()
            self._write_video_dict_to_disk(video_id=video_id, raw_data=video_data)
            post_details_result = self._build_post_details_result_from_video(video_data)
            self.cache.set(
                cache_key,
                post_details_result,
                expire=self.cache_expire_seconds,
            )

            return post_details_result

    def _write_user_dict_to_disk(self, account_id: str, raw_data: dict) -> None:
        if self.write_raw_data:
            with open(
                path.join(self.raw_data_folder, f"user_data_{account_id}.json"), "w"
            ) as f:
                json.dump(raw_data, f, indent=2)

    def _write_video_dict_to_disk(self, video_id: str, raw_data: dict) -> None:
        if self.write_raw_data:
            with open(
                path.join(self.raw_data_folder, f"video_data_{video_id}.json"), "w"
            ) as f:
                json.dump(raw_data, f, indent=2)

    def _video_cache_key(self, video_id: str) -> str:
        return f"tiktok_video_{video_id}"

    def _build_post_details_result_from_video(
        self,
        video_data: dict,
    ) -> PostDetailsExtractionResult:

        video_id = video_data["id"]
        author_unique_id = video_data["author"]["uniqueId"]
        video_url = f"https://www.tiktok.com/@{author_unique_id}/video/{video_id}"
        content_descs = "\n".join(
            [c.get("desc", "") for c in video_data.get("contents", [])]
        )
        videos_statsV2 = video_data.get("statsV2", {})
        return PostDetailsExtractionResult(
            data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
            post_url=video_url,
            title=video_data.get("desc", ""),
            description=content_descs,
            comment_count=int(videos_statsV2.get("commentCount", 0)),
            view_count=int(videos_statsV2.get("playCount", 0)),
            like_count=int(videos_statsV2.get("diggCount", 0)),
            repost_count=int(videos_statsV2.get("repostCount", 0)),
            share_count=int(videos_statsV2.get("shareCount", 0)),
            tags=video_data.get("channelTags", []),
            categories=video_data.get("diversificationLabels", []),
            sn_has_paid_placement=bool(video_data.get("isAd", False)),
            sn_brand="",  # TODO(Find sample videos where this can be extracted)
            post_type="video",
            text_content="",  # nto relevant for video posts
        )
