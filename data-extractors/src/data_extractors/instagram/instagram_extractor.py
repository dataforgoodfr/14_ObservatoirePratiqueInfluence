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
import time
import random
import datetime
from datetime import timezone
import logging

import instaloader
from instaloader import Post
import diskcache  # Replaced custom cache

logger = logging.getLogger(__name__)


class InstagramExtractor(DataExtractor):

    def __init__(self):
        self.L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            compress_json=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )
        # Initialize a persistent, SQLite-backed cache
        # You can adjust the size_limit (in bytes) if needed
        self.cache = diskcache.Cache("data/cache/instagram")

    def _create_post_details_from_post(
        self, post: instaloader.Post
    ) -> PostDetailsExtractionResult:
        """Helper to convert an Instaloader Post into a PostDetailsExtractionResult."""
        return PostDetailsExtractionResult(
            data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
            post_url=f"instagram.com/p/{post.shortcode}/",
            title=post.title if post.title else "No title",
            description=post.caption,
            comment_count=post.comments,
            view_count=0,  # No data on instagram
            like_count=post.likes,
            repost_count=0,  # No data on instagram
            share_count=0,  # No data on instagram
            tags=post.caption_hashtags,
            categories=["no_data"],
            sn_has_paid_placement=post.is_sponsored,
            sn_brand=",".join([sponso.username for sponso in post.sponsor_users]),
            post_type=post.typename,
            text_content=(
                "Tagged users: " + " @".join(post.tagged_users)
                if post.tagged_users
                else ""
            ),
        )

    def extract_account(
        self, task_config: ExtractAccountTaskConfig
    ) -> AccountExtractionResult:
        """Get account details."""
        try:
            logger.info(f"Extracting account for account_id: {task_config.account_id}")
            profile = instaloader.Profile.from_username(
                self.L.context, task_config.account_id
            )
            logger.debug(
                f"Successfully fetched instagram account: {task_config.account_id} | Business: {profile.business_category_name}",
            )

            return AccountExtractionResult(
                handle=task_config.account_id,
                data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                description=profile.biography,
                follower_count=profile.followers,
                following_count=profile.followees,
                post_count=0,  # Need to loop through NodeIterator, very long
                view_count=0,  # No insta data
                like_count=0,  # No insta data
                categories=["no_data"],
            )
        except Exception as e:
            logger.error(f"Failed to extract account for {task_config.account_id}: {e}")
            raise Exception(
                f"Failed to extract account for {task_config.account_id}"
            ) from e

    def extract_post_list(
        self, task_config: ExtractPostListTaskConfig
    ) -> PostListExtractionResult:
        try:
            logger.info(
                f"Extracting post list for account id: {task_config.account_id}, "
                f"published_after: {task_config.published_after}, "
                f"published_before: {task_config.published_before}",
            )
            posts = instaloader.Profile.from_username(
                self.L.context, task_config.account_id
            ).get_posts()

            posts_ret = []
            for i, post in enumerate(posts):
                d3 = post.date.replace(tzinfo=timezone.utc)
                if (i > 3) and (d3 < task_config.published_after):
                    break
                if (d3 < task_config.published_before) and (
                    d3 > task_config.published_after
                ):
                    posts_ret.append({"post_id": post.shortcode, "published_at": d3})

                    post_details = self._create_post_details_from_post(post)

                    # Save to cache with the shortcode as the key.
                    # Added a 14z-day expiration (60 * 60 * 24 * 14 seconds) so stale data naturally clears.
                    cache_key = f"post_{post.shortcode}"
                    self.cache.set(cache_key, post_details, expire=60 * 60 * 24 * 14)

                time.sleep(random.uniform(2, 6))

            logger.info(
                f"Returning {len(posts_ret)} posts for {task_config.account_id}"
            )
            return PostListExtractionResult(
                data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
                posts=posts_ret,
            )
        except Exception as e:
            logger.error(
                f"Failed to extract post list for {task_config.account_id}: {e}"
            )
            raise Exception(
                f"Failed to extract post list for {task_config.account_id}"
            ) from e

    def extract_post_details(
        self, task_config: ExtractPostDetailsTaskConfig
    ) -> PostDetailsExtractionResult:

        # Check cache first using the globally unique shortcode
        cache_key = f"post_{task_config.post_id}"
        cached_post = self.cache.get(cache_key)

        if cached_post:
            logger.info(f"CACHED_POST found for: {task_config.post_id}")
            return cached_post

        try:
            logger.info(f"Extracting post detail for post id: {task_config.post_id}")
            post = Post.from_shortcode(self.L.context, task_config.post_id)
            logger.debug(f"Fetched post: {post.title}")

            post_details = self._create_post_details_from_post(post)

            # Cache the newly fetched data
            self.cache.set(cache_key, post_details, expire=604800)
            return post_details

        except Exception as e:
            logger.error(
                f"Failed to extract post detail for {task_config.post_id}: {e}"
            )
            raise Exception(
                f"Failed to extract post detail for {task_config.post_id}"
            ) from e
