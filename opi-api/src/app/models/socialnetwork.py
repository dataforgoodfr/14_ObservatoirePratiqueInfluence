import pydantic


class Influencer(pydantic.BaseModel):
    uid: str
    username: str
