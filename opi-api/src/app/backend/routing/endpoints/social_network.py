import http

from fastapi import Response

from app._config import settings
from app.models import Account, Post
from app.nocodb import NocoDBClient


async def upsert_posts(posts: list[Post]) -> Response:
    client = NocoDBClient()
    for post in posts:
        client.upsert_record(
            "post",
            {
                "Account": {
                    "target_table": settings.nocodb_account_table,
                    "lookup": {
                        "Social Network": post.social_network,
                        "Account Id": post.account_id,
                    },
                },
            },
            {"Post Id": post.post_id},
            {
                "Social Network": post.social_network,
                "Post Id": post.post_id,
                "Post Url": post.post_url,
                "Title": post.title,
                "Description": post.description,
                "Comment Count": post.comment_count,
                "View Count": post.view_count,
                "Repost Count": post.repost_count,
                "Like Count": post.like_count,
                "Share Count": post.share_count,
                "Categories": post.categories,
                "Tags": post.tags,
                "SN Has Paid Placement": post.sn_has_paid_placement,
                "SN Brand": post.sn_brand,
                "Post Type": post.post_type,
            },
        )
    return Response(status_code=http.HTTPStatus.NO_CONTENT)


async def upsert_accounts(accounts: list[Account]) -> Response:
    client = NocoDBClient()
    for account in accounts:
        client.upsert_record(
            "account",
            {},
            {
                "Social Network": account.social_network,
                "Account Id": account.account_id,
            },
            {
                "Social Network": account.social_network,
                "Account Id": account.account_id,
                "Account Extraction Date": account.account_extracted_at,
                "Handle": account.handle,
                "Description": account.description,
                "Follower Count": account.follower_count,
                "Following Count": account.following_count,
                "Post Count": account.post_count,
                "View Count": account.view_count,
                "Like Count": account.like_count,
                "Categories": account.categories,
            },
        )
    return Response(status_code=http.HTTPStatus.NO_CONTENT)
