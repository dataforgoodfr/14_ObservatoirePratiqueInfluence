"""HTTP client for YouTube Data API v3."""

import datetime
from enum import StrEnum
import logging
from dataclasses import dataclass
from typing import Any

import requests

from .disk_cache import DiskCache
from .youtube_api_config import YoutubeApiConfig

logger = logging.getLogger(__name__)


class YoutubeApiError(Exception):
    """Base exception for YouTube API errors."""

    def __init__(
        self, message: str, status_code: int | None = None, response: dict | None = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class QuotaExceededError(YoutubeApiError):
    """Exception raised when API quota is exceeded."""

    pass


class ChannelNotFoundError(YoutubeApiError):
    """Exception raised when a channel cannot be found."""

    pass


class VideoNotFoundError(YoutubeApiError):
    """Exception raised when a video cannot be found."""

    pass


@dataclass
class Channel:
    """Represents a YouTube channel."""

    id: str
    title: str
    description: str
    subscriber_count: int
    video_count: int
    view_count: int
    topic_categories: list[str]
    uploads_playlist_id: str
    custom_url: str | None = None


@dataclass
class PlaylistItem:
    """Represents a single item in a YouTube playlist."""

    video_id: str
    title: str
    description: str
    published_at: datetime.datetime
    thumbnail_url: str | None = None


class YoutubePostType(StrEnum):
    VIDEO = "video"
    SHORT = "short"


def post_url(post_id: str, post_type: YoutubePostType) -> str:
    match post_type:
        case YoutubePostType.VIDEO:
            return "https://www.youtube.com/watch?v=" + post_id
        case YoutubePostType.SHORT:
            return "https://www.youtube.com/shorts/" + post_id


@dataclass
class Video:
    """Represents a YouTube video."""

    id: str
    title: str
    description: str
    published_at: datetime.datetime
    view_count: int
    like_count: int | None
    comment_count: int | None
    tags: list[str]
    duration: str
    post_type: YoutubePostType
    topic_categories: list[str]
    has_paid_placement: bool = False


class YoutubeApiClient:
    """Client for interacting with YouTube Data API v3 with disk caching support."""

    def __init__(self, config: YoutubeApiConfig):
        self.config = config
        self.session = requests.Session()
        self._disk_cache = DiskCache(config=config.cache_config)

    def get_channel_by_id(self, id: str) -> Channel:
        logger.debug("Fetch channel with id: %s", id)
        response = self._make_request(
            "channels",
            params={
                "part": "snippet,statistics,topicDetails,contentDetails",
                "id": id,
                "handleType": "channel",
            },
        )
        items = response.get("items", [])
        if not items:
            raise ChannelNotFoundError(f"Channel not found for id: {id}")
        return self._channel_from_response_item(items[0])

    def get_channel_by_handle(self, handle: str) -> Channel:
        logger.debug("Fetch channel for handle: %s", handle)
        response = self._make_request(
            "channels",
            params={
                "part": "snippet,statistics,topicDetails,contentDetails",
                "forHandle": handle,
                "handleType": "channel",
            },
        )
        items = response.get("items", [])
        if not items:
            raise ChannelNotFoundError(f"Channel not found for handle: {handle}")
        return self._channel_from_response_item(items[0])

    def get_channel_uploads_playlist_id(self, channel_id: str) -> str:
        channel = self.get_channel_by_id(channel_id)
        return channel.uploads_playlist_id

    def list_playlist_items(
        self,
        playlist_id: str,
        page_token: str | None = None,
        max_results: int = 50,
    ) -> tuple[list[PlaylistItem], str | None]:
        logger.debug("Fetch playlist items for playlist_id: %s", playlist_id)
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": min(max_results, 50),
        }

        if page_token:
            params["pageToken"] = page_token

        response = self._make_request("playlistItems", params)

        items = response.get("items", [])
        next_page_token = response.get("nextPageToken")

        results = []
        for item in items:
            snippet = item.get("snippet", {})
            results.append(
                PlaylistItem(
                    video_id=snippet.get("resourceId", {}).get("videoId", ""),
                    title=snippet.get("title", ""),
                    description=snippet.get("description", ""),
                    published_at=self._parse_datetime(snippet.get("publishedAt", "")),
                    thumbnail_url=snippet.get("thumbnails", {})
                    .get("default", {})
                    .get("url"),
                )
            )

        return results, next_page_token

    def list_all_playlist_items(self, playlist_id: str) -> list[PlaylistItem]:
        all_items = []
        page_token: str | None = None

        while True:
            items, page_token = self.list_playlist_items(playlist_id, page_token)
            all_items.extend(items)
            if not page_token:
                break

        return all_items

    def get_video(self, video_id: str) -> Video:
        videos = self._get_videos([video_id])
        return videos[0]

    def get_videos(self, video_ids: list[str]) -> list[Video]:
        page_size = 50
        video_ids_chunks = [
            video_ids[i : i + page_size] for i in range(0, len(video_ids), page_size)
        ]
        videos: list[Video] = list()
        for ids_chunk in video_ids_chunks:
            videos_chunk = self._get_videos(video_ids=ids_chunk)
            videos.extend(videos_chunk)
        return videos

    def _get_videos(self, video_ids: list[str]) -> list[Video]:
        logger.info("Fetching videos with id: %s", video_ids)
        assert len(video_ids) <= 50
        params = {
            "part": "snippet,statistics,contentDetails,paidProductPlacementDetails,topicDetails",
            "id": ",".join(video_ids),
            "maxResults": len(video_ids),
        }

        response = self._make_request("videos", params)

        items = response.get("items", [])
        if len(items) != len(video_ids):
            raise VideoNotFoundError(
                f"Unexpected results count for video ids: {video_ids}"
            )

        return [self._item_to_video(item) for item in items]

    def _item_to_video(self, video_respons_item: Any) -> Video:
        snippet = video_respons_item.get("snippet", {})
        statistics = video_respons_item.get("statistics", {})
        content_details = video_respons_item.get("contentDetails", {})
        paid_placement = video_respons_item.get("paidProductPlacementDetails", {})
        topic_details = video_respons_item.get("topicDetails", {})
        duration = content_details.get("duration", "PT0S")
        post_id = video_respons_item["id"]
        return Video(
            id=post_id,
            title=snippet.get("title", ""),
            description=snippet.get("description", ""),
            published_at=self._parse_datetime(snippet.get("publishedAt", "")),
            view_count=int(statistics.get("viewCount", 0)),
            like_count=statistics.get("likeCount"),
            comment_count=statistics.get("commentCount"),
            tags=snippet.get("tags", []),
            duration=duration,
            post_type=self._guess_post_type(post_id),
            topic_categories=topic_details.get("topicCategories", []),
            has_paid_placement=paid_placement.get("hasPaidProductPlacement", False),
        )

    def _guess_post_type(self, post_id: str) -> YoutubePostType:
        # Consider shorts if short HEAD request on short url respond with 200
        # See (https://stackoverflow.com/a/72197652)
        response = self.session.head(post_url(post_id, YoutubePostType.SHORT))
        if response.status_code == 200:
            return YoutubePostType.SHORT
        else:
            return YoutubePostType.VIDEO

    def _parse_datetime(self, date_str: str) -> datetime.datetime:
        if not date_str:
            return datetime.datetime.min
        return datetime.datetime.fromisoformat(date_str)

    def _channel_from_response_item(
        self, channels_response_item: dict[str, Any]
    ) -> Channel:
        snippet = channels_response_item.get("snippet", {})
        statistics = channels_response_item.get("statistics", {})
        topic_details = channels_response_item.get("topicDetails", {})

        return Channel(
            id=channels_response_item["id"],
            title=snippet.get("title", ""),
            description=snippet.get("description", ""),
            subscriber_count=int(statistics.get("subscriberCount", 0)),
            video_count=int(statistics.get("videoCount", 0)),
            view_count=int(statistics.get("viewCount", 0)),
            topic_categories=topic_details.get("topicCategories", []),
            custom_url=snippet.get("customUrl"),
            uploads_playlist_id=channels_response_item["contentDetails"][
                "relatedPlaylists"
            ]["uploads"],
        )

    def _make_request(
        self,
        endpoint: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        url = f"{self.config.base_url}/{endpoint}"
        params["key"] = self.config.api_key

        # Check cache first
        cached_data = self._disk_cache.get(url, params)
        if cached_data is not None:
            logger.debug(f"Cache hit for {endpoint}")
            return cached_data

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            response_data = response.json()

            # Cache successful response
            self._disk_cache.set(url, params, response_data)
            return response_data

        except requests.exceptions.HTTPError:
            if self._is_quota_exceeded_error(response):
                response_content = response.json() if response.content else {}
                raise QuotaExceededError(
                    "YouTube API quota exceeded",
                    status_code=response.status_code,
                    response=response_content,
                )
            else:
                raise YoutubeApiError(
                    f"HTTPError: {response.status_code} text: {response.text}",
                    status_code=response.status_code,
                )
        except requests.exceptions.RequestException as e:
            raise YoutubeApiError(f"Request failed: {e}")

    def _is_quota_exceeded_error(self, response: requests.Response) -> bool:
        if response.status_code == 403:
            error_data = response.json() if response.content else {}
            return (
                error_data.get("error", {}).get("errors", [{}])[0].get("reason")
                == "quotaExceeded"
            )
        else:
            return False
