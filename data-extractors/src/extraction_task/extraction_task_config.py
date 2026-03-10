from typing import Union
from pydantic import AwareDatetime, BaseModel


class ExtractPostDetailsTaskConfig(BaseModel):
    account_id: str
    post_id: str


class ExtractPostListTaskConfig(BaseModel):
    account_id: str
    published_after: AwareDatetime
    published_before: AwareDatetime


class ExtractAccountTaskConfig(BaseModel):
    account_id: str


ExtractionTaskConfig = Union[
    ExtractPostDetailsTaskConfig, ExtractPostListTaskConfig, ExtractAccountTaskConfig
]
