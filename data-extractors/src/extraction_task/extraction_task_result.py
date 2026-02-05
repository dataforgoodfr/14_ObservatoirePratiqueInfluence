from pydantic import AwareDatetime, BaseModel

from typing import Union


class AccountExtractionResult(BaseModel):
    data_extraction_date: AwareDatetime
    description: str
    follower_count: int
    following_count: int
    post_count: int
    view_count: int
    like_count: int
    categories: list[str]


class PostListResultItem(BaseModel):
    post_id: str
    published_at: AwareDatetime


class PostListExtractionResult(BaseModel):
    data_extraction_date: AwareDatetime
    posts: list[PostListResultItem]


class PostDetailsExtractionResult(BaseModel):
    data_extraction_date: AwareDatetime
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


ExtractionTaskResult = Union[
    AccountExtractionResult, PostListExtractionResult, PostDetailsExtractionResult
]
