from typing import Union
from pydantic import AwareDatetime, BaseModel


class ExtractPostDetailsTaskConfig(BaseModel):
    post_id: str


class ExtractPostListTaskConfig(BaseModel):
    account_id: str
    published_after: AwareDatetime
    published_before: AwareDatetime


class ExtractAccountTaskConfig(BaseModel):
    # FIXME this should be an account id rather than a handle
    account_id: str


ExtractionTaskConfig = Union[
    ExtractPostDetailsTaskConfig, ExtractPostListTaskConfig, ExtractAccountTaskConfig
]
