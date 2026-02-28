from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nocodb_url: str
    nocodb_api_token: str
    nocodb_base_id: str
    nocodb_account_table: str
    nocodb_post_table: str


settings = Settings()
