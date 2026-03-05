import asyncio
from collections import defaultdict
import datetime
import logging
import os
import random
from playwright.async_api import async_playwright

from TikTokApi import TikTokApi


logger = logging.getLogger(__name__)


async def get_ms_tokens() -> list[str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
        )
        page = await browser.new_page()

        await page.goto(
            "https://tiktok.com/explore",
            wait_until="domcontentloaded",
        )

        cookies_string: str = ""
        while "msToken" not in cookies_string:
            cookies_string = await page.evaluate("document.cookie")
            await page.wait_for_timeout(500)

        logger.info(f"cookies_string: {cookies_string}")

        cookies = defaultdict(list)
        for pair in cookies_string.split("; "):
            if pair:
                key, value = pair.split("=", 1)
                cookies[key].append(value)

        ms_tokens = cookies["msToken"]

        logger.info(f"ms_tokens: {ms_tokens}")

        await browser.close()
        return ms_tokens


# TIKTOK maximum number of pinned videos
MAX_PINNED = 3


async def get_videos_for_date_range(
    user: TikTokApi.user,
    published_after: datetime.datetime,
    published_before: datetime.datetime,
) -> list[TikTokApi.video]:

    videos: list[TikTokApi.video] = []
    offset = 0

    # user.videos uses async iterators so we can set an very large max_videos they will only be fetched if we don't stop before
    max_videos = 100000
    logger.info(f"Fetching videos for {user.username}")

    index = 0
    if published_before > datetime.datetime.now():
        cursor = 0
    else:
        # This is not documented but tiktok cursor looks like an epoch *1000
        cursor = round(published_before.timestamp() * 1000)

    # Videos are ordered chronologically from most recent to oldest
    # Except for the first MAX_PINNED  videos when cursor=0 which can be older pinned videos
    async for video in user.videos(count=max_videos, cursor=cursor):
        if published_after <= video.create_time <= published_before:
            logger.info(
                f"Adding in range video {video.id} - created at {video.create_time}"
            )
            videos.append(video)
        elif (
            published_after > video.create_time
            and cursor == 0
            and index + offset < MAX_PINNED
        ):
            logger.info(
                f"Skipping potentially pinned before range video {video.id} - created at {video.create_time}"
            )
        elif published_after > video.create_time:
            logger.info(
                f"Stopping at before range video {video.id} created at {video.create_time}"
            )
            return videos
        else:
            logger.info(
                f"Skipping after range video {video.id} - created at {video.create_time}"
            )

        random_sleep = random.uniform(1, 3)
        logger.info(f"Sleeping for random duration {random_sleep}s")
        await asyncio.sleep(random_sleep)
        index += 1

    raise Exception("With reached the max_videos defined!!!")


async def create_sessions(api: TikTokApi) -> None:
    env_ms_token = os.getenv("TIKTOK_MS_TOKEN")
    headless = os.getenv("TIKTOK_HEADLESS", "False").lower() == "true"
    if env_ms_token is None:
        ms_tokens = None
    elif env_ms_token.lower() == "playwright":
        ms_tokens = await get_ms_tokens()
    else:
        ms_tokens = [env_ms_token]
    await api.create_sessions(
        ms_tokens=ms_tokens,
        num_sessions=1,
        sleep_after=3,
        timeout=60000,
        browser="chromium",
        headless=headless,
    )
