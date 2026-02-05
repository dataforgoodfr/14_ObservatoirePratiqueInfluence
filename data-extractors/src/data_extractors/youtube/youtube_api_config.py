"""Configuration for YouTube API client."""

from dataclasses import dataclass

from data_extractors.youtube.disk_cache import DiskCacheConfig


@dataclass
class YoutubeApiConfig:
    """Configuration for YouTube API client.

    Args:
        api_key: YouTube Data API v3 API key
        base_url: Base URL for YouTube API (default: https://www.googleapis.com/youtube/v3)
        cache_config: configure request caching on disk
    """

    api_key: str
    cache_config: DiskCacheConfig
    base_url: str = "https://www.googleapis.com/youtube/v3"
