"""Disk-based cache for HTTP responses with configurable TTL."""

from dataclasses import dataclass
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)


@dataclass
class DiskCacheConfig:
    cache_dir: str
    ttl_seconds: int = 3600 * 24 * 3  # 3 days cache
    cleanup_interval_seconds: int = 3600 * 24  # daily cleanup
    enabled: bool = True
    ignored_request_params: frozenset[str] = frozenset({"key"})


class DiskCache:
    """Disk-based cache for HTTP responses."""

    def __init__(self, config: DiskCacheConfig):
        """Initialize disk cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Default TTL for cache entries in seconds
            enabled: Whether to enable caching
            ignored_params: params ignored while computing cache hash key
            cleanup_interval_seconds: Interval in seconds to trigger cleanup on set.
                If None, cleanup is not triggered automatically on set.
        """
        self.cache_dir = Path(config.cache_dir)
        self.ttl_seconds = config.ttl_seconds
        self.enabled = config.enabled
        self.ignored_params = config.ignored_request_params
        self.cleanup_interval_seconds = config.cleanup_interval_seconds
        self._last_cleanup_time = 0.0
        self._ensure_cache_dir()

    def _ensure_cache_dir(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, url: str, params: dict[str, Any]) -> str:
        """Generate cache key from URL and params using SHA256 hash."""
        # Create a copy without ignored_params for cache sharing
        cache_params = {k: v for k, v in params.items() if k not in self.ignored_params}
        # Sort params for consistent hashing
        sorted_params = json.dumps(cache_params, sort_keys=True)
        hash_input = f"{url}:{sorted_params}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:32]

    def _get_cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, url: str, params: dict[str, Any]) -> dict[str, Any] | None:
        """Get cached response if not expired.

        Args:
            url: The API endpoint URL
            params: Query parameters

        Returns:
            The cached response or None if not found/expired
        """
        if not self.enabled:
            return None

        key = self._get_cache_key(url, params)
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            cached_at = cache_data.get("cached_at", 0)
            data = cache_data.get("data")

            if data is None:
                return None

            current_time = time.time()
            expires_at = cached_at + self.ttl_seconds
            is_stale = current_time > expires_at

            if is_stale:
                logger.debug(f"Cache stale for key {key}, expires at {expires_at}")
                return None

            logger.debug(f"Cache hit for key {key}")
            return data
        except (json.JSONDecodeError, KeyError, OSError) as e:
            logger.warning(f"Failed to read cache for key {key}: {e}")
            return None

    def set(
        self,
        url: str,
        params: dict[str, Any],
        data: dict[str, Any],
    ) -> None:
        """Cache response.

        Args:
            url: The API endpoint URL
            params: Query parameters
            data: Response data to cache
        """
        if not self.enabled:
            return

        key = self._get_cache_key(url, params)
        cache_path = self._get_cache_path(key)

        cache_data = {
            "key": key,
            "url": url,
            "params": {k: v for k, v in params.items() if k != "key"},
            "cached_at": time.time(),
            "data": data,
        }

        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
            logger.debug(f"Cached response for url {url} with key {key}s")
        except OSError as e:
            logger.warning(f"Failed to write cache for key {key}: {e}")

        self._maybe_cleanup()

    def _maybe_cleanup(self) -> None:
        """Trigger cleanup if the interval has elapsed since last cleanup."""
        if self.cleanup_interval_seconds is None:
            return

        current_time = time.time()
        if current_time - self._last_cleanup_time >= self.cleanup_interval_seconds:
            self.cleanup_expired()
            self._last_cleanup_time = current_time

    def cleanup_expired(self) -> int:
        if not self.cache_dir.exists():
            return 0

        current_time = time.time()
        removed = 0

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)

                cached_at = cache_data.get("cached_at", 0)

                if current_time > cached_at + self.ttl_seconds:
                    cache_file.unlink()
                    removed += 1

            except (json.JSONDecodeError, KeyError, OSError):
                # Remove corrupted cache files
                try:
                    cache_file.unlink()
                    removed += 1
                except OSError:
                    pass

        logger.info(f"Cleanup expired removed {removed} cache entries")
        return removed
