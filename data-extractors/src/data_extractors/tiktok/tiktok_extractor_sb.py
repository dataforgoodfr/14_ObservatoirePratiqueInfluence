import datetime
from datetime import timedelta
import json
import logging
import random
import time

from os import path
from pathlib import Path

import diskcache

from seleniumbase import SB
from selenium.webdriver.common.by import By

from data_extractors.data_extractor import DataExtractor

from data_extractors.tiktok.tiktok_sb import Video

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


class TiktokExtractorSB(DataExtractor):
    def __init__(
        self,
        cache_folder: str,
        cache_ttl_seconds: int,
        write_raw_data_to_disk: bool = False,
    ) -> None:
        self.cache = diskcache.Cache(
            directory=cache_folder,
        )
        self.cache_ttl_seconds = cache_ttl_seconds
        # Whether to store raw API data for further analysis/reuse
        self.write_raw_data = write_raw_data_to_disk
        if write_raw_data_to_disk:
            self.raw_data_folder = Path(path.join(cache_folder, "raw_data"))
            self.raw_data_folder.mkdir(parents=True, exist_ok=True)

    def extract_account(
        self,
        task_config: ExtractAccountTaskConfig,
    ) -> AccountExtractionResult:
        try:
            with SB(uc=True, headless=True) as sb:
                acct = task_config.account_id
                tiktok_url = f"https://www.tiktok.com/@{acct}"

                sb.driver.uc_open_with_reconnect(tiktok_url, reconnect_time=4)

                userstatsV2_xpath = '//script[@id="__UNIVERSAL_DATA_FOR_REHYDRATION__"]'

                userstatsV2 = sb.driver.find_element(By.XPATH, userstatsV2_xpath)

                user_cmplt_json = json.loads(userstatsV2.get_attribute("innerHTML"))
                user_data = user_cmplt_json["__DEFAULT_SCOPE__"]["webapp.user-detail"][
                    "userInfo"
                ]

                user_info_user = user_data["user"]
                user_info_statsV2 = user_data["statsV2"]

                self._write_user_dict_to_disk(task_config.account_id, user_data)

                return AccountExtractionResult(
                    data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                    handle=user_info_user["uniqueId"],
                    description=user_info_user["signature"]
                    .encode("cp1252", errors="ignore")
                    .decode("cp1252"),
                    follower_count=int(user_info_statsV2["followerCount"]),
                    following_count=int(user_info_statsV2["followingCount"]),
                    post_count=int(user_info_statsV2["videoCount"]),
                    like_count=int(user_info_statsV2["heartCount"]),
                    view_count=0,  # not availabled at user level
                    categories=[],  # not availabled
                )
        except Exception as e:
            message = f"Failed to extract account details for account id: {task_config.account_id}"
            logger.exception(message)
            raise TiktokExtractionException(message) from e

    def extract_post_list(
        self, task_config: ExtractPostListTaskConfig
    ) -> PostListExtractionResult:
        """Extract list of posts from a TikTok account within a date range.

        Uses Seleniumbase to fetch user videos and filters afterwards
        by published_after/published_before.
        """

        logger.info(
            f"Extracting post list for account_id: {task_config.account_id}, "
            f"published_after: {task_config.published_after}, "
            f"published_before: {task_config.published_before}"
        )

        posts: list[PostListResultItem] = []

        try:
            with SB(uc=True, headless=False) as sb:
                acct = task_config.account_id
                tiktok_url = f"https://www.tiktok.com/@{acct}"

                sb.driver.uc_open_with_reconnect(tiktok_url, reconnect_time=4)

                item_xpath = '//div[contains(@id, "grid-item-container")]'

                while True:
                    items = sb.driver.find_elements(By.XPATH, f"{item_xpath}")
                    try:
                        _ = items[-1]  # Verify items are loaded
                        break
                    except IndexError:
                        logger.info("Scrapper detected, cooldown")
                        time.sleep(10 * random.randint(50, 65))

                        sb.driver.uc_open_with_reconnect(tiktok_url, reconnect_time=4)
                        logger.info("Reopen webpage and wait to load posts")
                        time.sleep(20)

                div_ancestors = '//div[@id="user-post-item-list"]'
                post_xpath = '//a[contains(@href, "/video/")]'

                posts_elements = sb.driver.find_elements(
                    By.XPATH, f"{div_ancestors}{post_xpath}"
                )

                last_video = Video(posts_elements[-1])

                while last_video.date > task_config.published_after - timedelta(days=1):
                    sb.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )

                    time.sleep(random.randint(2, 8))

                    posts_elements = sb.driver.find_elements(
                        By.XPATH, f"{div_ancestors}{post_xpath}"
                    )

                    last_post_element = posts_elements[-1]
                    last_video = Video(last_post_element)

                all_posts = sb.driver.find_elements(
                    By.XPATH, f"{div_ancestors}{post_xpath}"
                )

                time.sleep(random.randint(1, 20))

                all_videos = [Video(post) for post in all_posts]

                videos = [
                    v
                    for v in all_videos
                    if task_config.published_after <= v.date
                    and v.date <= task_config.published_before
                ]

                posts = [
                    PostListResultItem(
                        post_id=v.id,
                        published_at=v.date,
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
            message = (
                f"Failed to extract post list for account id: {task_config.account_id}, "
                + f"published_after: {task_config.published_after}, published_before: {task_config.published_before}"
            )
            logger.exception(message)
            raise TiktokExtractionException(message) from e

    def extract_post_details(
        self,
        task_config: ExtractPostDetailsTaskConfig,
    ) -> PostDetailsExtractionResult:

        try:
            video_id = task_config.post_id
            cache_key = self._video_cache_key(task_config.post_id)
            cached_value = self.cache.get(cache_key)
            if cached_value:
                logger.info(f"CACHED_POST found for: {video_id}")
                return cached_value

            with SB(uc=True, headless=True) as sb:
                user_agnostic_video_url = (
                    f"https://www.tiktok.com/@tiktok/video/{video_id}"
                )
                sb.driver.uc_open_with_reconnect(user_agnostic_video_url)

                videostatsV2_xpath = (
                    '//script[@id="__UNIVERSAL_DATA_FOR_REHYDRATION__"]'
                )
                videostatsV2 = sb.driver.find_element(By.XPATH, videostatsV2_xpath)
                video_cmplt_json = json.loads(videostatsV2.get_attribute("innerHTML"))

                video_data = video_cmplt_json["__DEFAULT_SCOPE__"][
                    "webapp.video-detail"
                ]["itemInfo"]["itemStruct"]

                self._write_video_dict_to_disk(video_id=video_id, raw_data=video_data)

                post_details_result = self._build_post_details_result_from_video(
                    video_data
                )
                self.cache.set(
                    cache_key,
                    post_details_result,
                    expire=self.cache_ttl_seconds,
                )

                return post_details_result
        except Exception as e:
            message = (
                f"Failed to extract post details for video id: {task_config.post_id}"
            )
            logger.exception(message)
            raise TiktokExtractionException(message) from e

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
            [
                (c.get("desc", "")).encode("cp1252", errors="ignore").decode("cp1252")
                for c in video_data.get("contents", [])
            ]
        )

        videos_statsV2 = video_data.get("statsV2", {})
        return PostDetailsExtractionResult(
            data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
            post_url=video_url,
            title=(video_data.get("desc", ""))
            .encode("cp1252", errors="ignore")
            .decode("cp1252"),
            description=content_descs,
            comment_count=int(videos_statsV2.get("commentCount", 0)),
            view_count=int(videos_statsV2.get("playCount", 0)),
            like_count=int(videos_statsV2.get("diggCount", 0)),
            repost_count=int(videos_statsV2.get("repostCount", 0)),
            share_count=int(videos_statsV2.get("shareCount", 0)),
            tags=video_data.get("channelTags", []),
            categories=video_data.get("diversificationLabels", []),
            sn_has_paid_placement=bool(video_data.get("isAdVirtual", False)),
            sn_brand="",  # TODO(Find sample videos where this can be extracted)
            post_type="video",
            text_content="",  # nto relevant for video posts
        )


class TiktokExtractionException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
