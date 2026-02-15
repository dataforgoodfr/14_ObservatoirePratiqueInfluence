import datetime
from itertools import dropwhile, takewhile
from datetime import timezone

import instaloader

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    compress_json=False,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
)

posts = instaloader.Profile.from_username(L.context, "carlamoreau_____").get_posts()

published_after = datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
published_before = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)


SINCE = published_after
UNTIL = published_before
posts_ret = []

"""
for post in takewhile(
    lambda p: p.date.replace(tzinfo=timezone.utc) < UNTIL,
    dropwhile(lambda p: p.date.replace(tzinfo=timezone.utc) > SINCE, posts),
):
"""
for post in posts:
    d1 = SINCE
    d2 = UNTIL
    d3 = post.date.replace(tzinfo=timezone.utc)
    print(d1)
    if (d3 > d1) & (d3 < d2):
        print("=" * 10)
        print(d3)
        posts_ret.append({"post_id": post.shortcode, "published_at": d3})
        print("=" * 10)
