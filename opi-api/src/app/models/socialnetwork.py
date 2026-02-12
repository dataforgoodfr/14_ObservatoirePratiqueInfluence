from enum import StrEnum

import pydantic


class SocialNetwork(StrEnum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"


class Influencer(pydantic.BaseModel):
    uid: str
    username: str
