import datetime
import json
import requests
import logging

from bs4 import BeautifulSoup

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
)

logger = logging.getLogger(__name__)


class TiktokExtractor(DataExtractor):
    def __init__(self, browser_name=None):
        self.headers = {
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "referer": "https://www.tiktok.com/",
        }

    def extract_account(
        self,
        task_config: ExtractAccountTaskConfig,
    ) -> AccountExtractionResult:
        response = requests.get(
            f"https://www.tiktok.com/@{task_config.account_id}",
            allow_redirects=True,  # may have to set to True
            headers=self.headers,
            timeout=20,
            stream=False,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        rehydration_data = soup.find(
            "script", attrs={"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"}
        )

        rehydration_data_json = json.loads(rehydration_data.string)

        # filtering html data
        try:
            user_data = rehydration_data_json["__DEFAULT_SCOPE__"][
                "webapp.user-detail"
            ]["userInfo"]
            user_info = user_data["user"]
            user_stats = user_data["statsV2"]

            return AccountExtractionResult(
                data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                handle=user_info.get("nickname", ""),
                description=user_info.get("signature", ""),
                follower_count=int(user_stats.get("followerCount", 0)),
                following_count=int(user_stats.get("followingCount", 0)),
                post_count=int(user_stats.get("videoCount", 0)),
                view_count=0,  # Not available for tiktok
                like_count=int(user_stats.get("heartCount", 0)),
                categories=[],  # Not available for tiktok
            )
        except KeyError:
            logger.exception(f"Failed to extract account {task_config.account_id}")
            raise

    def extract_post_list(
        self, task_config: ExtractPostListTaskConfig
    ) -> PostListExtractionResult:
        raise Exception("TiktokDataExtractor.extract_post_list not implemented yet")

    def extract_post_details(
        self,
        task_config: ExtractPostDetailsTaskConfig,
    ) -> PostDetailsExtractionResult:
        script_tag = None
        post_url = f"https://www.tiktok.com/@tiktok/video/{task_config.post_id}"
        response = requests.get(
            f"https://www.tiktok.com/@tiktok/video/{task_config.post_id}",
            allow_redirects=True,  # may have to set to True
            headers=self.headers,
            timeout=20,
            stream=False,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")

        if script_tag is None:
            raise KeyError("__UNIVERSAL_DATA_FOR_REHYDRATION__ not in response")

        data = json.loads(script_tag.string)
        post_data = data["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"][
            "itemStruct"
        ]
        post_stats = post_data["statsV2"]

        return PostDetailsExtractionResult(
            data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
            post_url=post_url,
            title="",  # Only description for tiktok
            description=post_data["desc"],
            comment_count=int(post_stats.get("commentCount", 0)),
            view_count=int(post_stats.get("playCount", 0)),
            like_count=int(post_stats.get("diggCount", 0)),
            repost_count=int(post_stats.get("repostCount", 0)),
            share_count=int(post_stats.get("shareCount", 0)),
            tags=post_data.get("channelTags", []),
            categories=post_data.get("diversificationLabels", []),
            sn_has_paid_placement=bool(post_data.get("isAd", False)),
            sn_brand="",  # youtube does not provide brand info for product placement
            post_type="video",
            text_content="",  # not relevant for video posts
        )
