from typing import Optional, Self, cast
from pydantic import AwareDatetime, BaseModel
from extraction_task import social_network
from extraction_task.local import csv_repository


class PostListItem(BaseModel):
    social_network: social_network.SocialNetwork
    post_id: str
    account_id: str

    @classmethod
    def from_csv_row(cls, csv_row: dict) -> Self:
        return cast(Self, PostListItem.model_validate(csv_row))

    def to_csv_row(self) -> dict:
        return self.model_dump()


class PostDetails(BaseModel):
    social_network: social_network.SocialNetwork
    post_id: str
    post_extraction_date: Optional[AwareDatetime]
    title: Optional[str]
    description: Optional[str]
    comment_count: Optional[int]
    view_count: Optional[int]
    repost_count: Optional[int]
    like_count: Optional[int]
    share_count: Optional[int]
    categories: list[str]
    tags: list[str]
    sn_has_paid_placement: Optional[bool]
    sn_brand: Optional[str]
    post_type: Optional[str]
    text_content: Optional[str]

    @classmethod
    def from_csv_row(cls, csv_row: dict) -> Self:
        model_data = csv_row.copy()
        model_data["categories"] = model_data["categories"].split(",")
        model_data["tags"] = model_data["tags"].split(",")
        for key in model_data:
            if model_data[key] == "":
                model_data[key] = None
        return cast(Self, PostDetails.model_validate(model_data))

    def to_csv_row(self) -> dict:
        row_data = self.model_dump()
        row_data["categories"] = ",".join(row_data["categories"])
        row_data["tags"] = ",".join(row_data["tags"])
        return row_data


class PostRepository:
    _csv_repository: csv_repository.CsvRowRepository

    def __init__(self, csv_file: str):
        field_names = list(
            dict.fromkeys(
                list(PostListItem.model_fields.keys())
                + list(PostDetails.model_fields.keys())
            )
        )

        self._csv_repository = csv_repository.CsvRowRepository(
            csv_file,
            field_names,
        )

    def _item_from_csv_row(self, csv_row: dict) -> PostListItem:
        return PostListItem.model_validate(csv_row)

    def _item_to_csv_row(self, item: PostListItem) -> dict:
        return item.model_dump()

    def upsert_post_list_item(self, post: PostListItem) -> None:
        def match_predicate(row: dict) -> bool:
            row_post = PostListItem.from_csv_row(row)
            return (
                row_post.post_id == post.post_id
                and row_post.social_network == post.social_network
            )

        self._csv_repository._upsert_row(
            match_predicate,
            post.model_dump(),
        )

    def upsert_post_details(self, post: PostDetails) -> None:
        def match_predicate(row: dict) -> bool:
            row_post = PostDetails.from_csv_row(row)
            return (
                row_post.post_id == post.post_id
                and row_post.social_network == post.social_network
            )

        self._csv_repository._upsert_row(
            match_predicate,
            post.model_dump(),
        )
