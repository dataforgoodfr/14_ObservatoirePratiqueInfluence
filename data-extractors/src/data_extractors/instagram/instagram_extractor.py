from pydantic import AwareDatetime

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
from instaloader import NodeIterator, Post

logger = logging.getLogger(__name__)


class InstagramExtractor(DataExtractor):
    def __init__(self) -> None:
        self.L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            compress_json=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )

    def _create_post_details_from_post(
        self, post: instaloader.Post
    ) -> PostDetailsExtractionResult:
        """Helper to convert an Instaloader Post into a PostDetailsExtractionResult."""
        return PostDetailsExtractionResult(
            post_id=post.shortcode,
            data_extraction_date=datetime.datetime.now(datetime.timezone.utc),
            post_url=f"instagram.com/p/{post.shortcode}/",
            title=post.title if post.title else "No title",
            description=post.caption if post.caption is not None else "",
            comment_count=post.comments,
            view_count=post.video_view_count
            if post.is_video and post.video_view_count
            else 0,  # No data for non video posts on instagram
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
            profile = instaloader.Profile.from_username(
                self.L.context, task_config.account_id
            )

            logger.info("Fetching instagram posts...")
            posts: list[PostDetailsExtractionResult] = (
                self._fetch_post_details_from_iterator(
                    profile.get_posts(),
                    task_config.published_after,
                    task_config.published_before,
                    f"[{task_config.account_id}][posts]",
                )
            )

            logger.info("Fetching instagram reels...")
            reels: list[PostDetailsExtractionResult] = (
                self._fetch_post_details_from_iterator(
                    profile.get_reels(),
                    task_config.published_after,
                    task_config.published_before,
                    f"[{task_config.account_id}][reels]",
                )
            )
            all_posts = posts + reels
            logger.info(
                f"Returning {len(all_posts)} posts ({len(posts)} posts and {len(reels)} reels) for {task_config.account_id}"
            )

            return PostListExtractionResult(
                posts=all_posts,
            )
        except Exception as e:
            logger.error(
                f"Failed to extract post list for {task_config.account_id}: {e}"
            )
            raise Exception(
                f"Failed to extract post list for {task_config.account_id}"
            ) from e

    def _fetch_post_details_from_iterator(
        self,
        posts_iterator: NodeIterator[Post],
        published_after: AwareDatetime,
        published_before: AwareDatetime,
        log_prefix: str,
    ) -> list[PostDetailsExtractionResult]:
        posts_ret: list[PostDetailsExtractionResult] = []
        start_time = datetime.datetime.now()
        span_to_cover_duration = start_time.timestamp() - published_after.timestamp()

        for index, post in enumerate(posts_iterator):
            post_date = post.date.replace(tzinfo=timezone.utc)
            progress_percent = (
                round(
                    100
                    * (start_time.timestamp() - post_date.timestamp())
                    / span_to_cover_duration
                )
                if span_to_cover_duration > 0
                else 100
            )
            base_log_message = (
                log_prefix
                + f"[{progress_percent:.0f}%] post {post.shortcode}[{post_date}]"
            )

            if published_after <= post_date <= published_before:
                post_details = self._create_post_details_from_post(post)
                posts_ret.append(post_details)
                logger.info(
                    base_log_message + f" - added as {len(posts_ret)}th post in range"
                )
            elif published_after > post_date and index < MAX_PINNED:
                # On instagram, users can pin up to 3 posts on their profiles.
                # So when scrapping a profile, the posts 1, 2 and 3 can be posts from any dates.
                logger.info(
                    base_log_message + " - skipped (before range but in MAX_PINNED)"
                )
            elif published_after > post_date and index >= MAX_PINNED:
                # The posts are ranked in a chronological ordrer from the most recent to the oldest (appart from the pinned posts).
                # We need to stop collecting posts whenever we reach a post with a date under our published_after date and that this post is not part of the 3 pinned posts.
                logger.info(base_log_message + " - we are done (before range).")
                break
            else:
                logger.info(base_log_message + " - ignoring (after range).")

            random_sleep = random.uniform(2, 6)
            logger.debug(f"Sleeping for random duration {random_sleep:0.1f}s")
            time.sleep(random_sleep)

        # End of cursor reached
        fetch_duration = datetime.datetime.now().timestamp() - start_time.timestamp()
        average_speed = len(posts_ret) / fetch_duration if fetch_duration > 0 else 0

        logger.info(
            log_prefix
            + f" - fetch_posts took {(fetch_duration / 1000):.0f}s for {len(posts_ret)} posts ({average_speed:.2f} posts/s)."
        )
        return posts_ret

    def extract_post_details(
        self, task_config: ExtractPostDetailsTaskConfig
    ) -> PostDetailsExtractionResult:

        try:
            logger.info(f"Extracting post detail for post id: {task_config.post_id}")
            post = Post.from_shortcode(self.L.context, task_config.post_id)
            logger.debug(f"Fetched post: {post.title}")
            post_details = self._create_post_details_from_post(post)
            return post_details

        except Exception as e:
            logger.error(
                f"Failed to extract post detail for {task_config.post_id}: {e}"
            )
            raise Exception(
                f"Failed to extract post detail for {task_config.post_id}"
            ) from e


# INstagram max pinned
MAX_PINNED = 3
