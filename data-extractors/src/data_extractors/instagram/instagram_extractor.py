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

            posts_ret: list[PostDetailsExtractionResult] = []
            for i, post in enumerate(posts):
                d3 = post.date.replace(tzinfo=timezone.utc)
                # On instagram, users can pin up to 3 posts on their profiles.
                # So when scrapping a profile, the posts 1, 2 and 3 can be posts from any dates.
                # Additionnaly the posts are ranked in a chronological ordrer from the most recent to the oldest (appart from the first 3 ones).
                # So we need to stop collecting posts whenever we reach a post with a date under our published_after date and that this post is not part of the 3 pinned posts.
                if (i > 3) and (d3 < task_config.published_after):
                    break
                if (d3 < task_config.published_before) and (
                    d3 > task_config.published_after
                ):
                    post_details = self._create_post_details_from_post(post)
                    posts_ret.append(post_details)

                time.sleep(random.uniform(2, 6))

            logger.info(
                f"Returning {len(posts_ret)} posts for {task_config.account_id}"
            )
            return PostListExtractionResult(
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
