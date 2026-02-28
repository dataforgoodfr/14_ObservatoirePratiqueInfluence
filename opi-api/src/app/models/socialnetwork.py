"""Social network models."""

from enum import StrEnum
from typing import Annotated

import pydantic


class SocialNetwork(StrEnum):
    """Available social networks."""

    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"


class Influencer(pydantic.BaseModel):
    """Influencer model."""

    uid: str
    username: str


class Account(pydantic.BaseModel):
    """Account model."""

    account_extracted_at: Annotated[
        pydantic.AwareDatetime, pydantic.PlainSerializer(lambda d: d.isoformat())
    ]
    account_id: str
    social_network: str
    handle: str | None
    description: str
    follower_count: int
    following_count: int
    post_count: int
    view_count: int
    like_count: int
    categories: list[str]


class Post(pydantic.BaseModel):
    """Post model."""

    post_extracted_at: Annotated[
        pydantic.AwareDatetime, pydantic.PlainSerializer(lambda d: d.isoformat())
    ]
    social_network: str
    account_id: str
    post_id: str
    post_url: str
    title: str
    description: str
    comment_count: int
    view_count: int
    repost_count: int
    like_count: int
    share_count: int
    categories: list[str]
    tags: list[str]
    sn_has_paid_placement: bool
    sn_brand: str
    post_type: str
    text_content: str
