"""Typed HTTP client for the OPI API.

This client provides strongly-typed methods matching the server endpoints
defined in opi-api/src/app/backend/routing/router.py.
"""

from enum import StrEnum
from typing import Any, Optional
from uuid import UUID

import requests
from pydantic import AwareDatetime, BaseModel
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class SocialNetwork(StrEnum):
    """Available social networks."""

    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"


class ExtractionTaskType(StrEnum):
    """Types of extraction tasks."""

    EXTRACT_ACCOUNT = "extract-account"
    EXTRACT_POST_LIST = "extract-post-list"
    EXTRACT_POST_DETAILS = "extract-post-details"


class ExtractionTaskStatus(StrEnum):
    """Available task statuses."""

    AVAILABLE = "AVAILABLE"
    ACQUIRED = "ACQUIRED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class _ExtractPostDetailsTaskConfig(BaseModel):
    post_id: str
    account_id: str


class _ExtractPostListTaskConfig(BaseModel):
    account_id: str
    published_after: AwareDatetime
    published_before: AwareDatetime


class _ExtractAccountTaskConfig(BaseModel):
    account_id: str


ExtractionTaskConfig = (
    _ExtractPostDetailsTaskConfig
    | _ExtractPostListTaskConfig
    | _ExtractAccountTaskConfig
)


class ExtractionTask(BaseModel):
    uid: UUID | None = None
    social_network: SocialNetwork
    type: ExtractionTaskType
    task_config: ExtractionTaskConfig
    status: ExtractionTaskStatus | None = None
    visible_at: AwareDatetime | None = None
    error: str | None = None


class ExtractionTaskResponse(BaseModel):
    task_uid: UUID | None = None
    social_network: SocialNetwork | None = None
    visible_at: AwareDatetime | None = None
    type: ExtractionTaskType | None = None
    task_config: ExtractionTaskConfig | None = None
    error: str | None = None


class Account(BaseModel):
    account_extracted_at: AwareDatetime
    account_id: str
    social_network: str
    handle: str | None = None
    description: str
    follower_count: int
    following_count: int
    post_count: int
    view_count: int
    like_count: int
    categories: list[str]


class Post(BaseModel):
    post_extracted_at: AwareDatetime
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


class AcquireTaskRequest(BaseModel):
    """Request body for acquiring a task."""

    social_network: str | None = None


class ApiClient:
    def __init__(self, api_url: str, api_token: str) -> None:
        self.api_url = api_url.rstrip("/")
        self.api_token = api_token
        self._session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        session.mount("http://", HTTPAdapter(max_retries=retry))
        session.mount("https://", HTTPAdapter(max_retries=retry))
        return session

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[Any] = None,
    ) -> requests.Response:
        """Make an HTTP request."""
        url = f"{self.api_url}{path}"
        response = self._session.request(
            method=method,
            url=url,
            headers=self._get_headers(),
            params=params,
            json=json,
        )
        response.raise_for_status()
        return response

    def acquire_task(
        self, social_network: SocialNetwork | None = None
    ) -> ExtractionTaskResponse:

        request_body = AcquireTaskRequest(
            social_network=social_network.value if social_network else None
        )
        response = self._request(
            "POST",
            "/extraction-task/acquire",
            json=request_body.model_dump(exclude_none=True),
        )
        return ExtractionTaskResponse.model_validate(response.json())

    def update_task(self, task_id: UUID, status: ExtractionTaskStatus) -> None:

        self._request(
            "PATCH",
            f"/extraction-task/{task_id}",
            params={"status": status.value},
        )

    def register_tasks(self, tasks: list[ExtractionTask]) -> list[ExtractionTask]:

        json_data = [task.model_dump(mode="json") for task in tasks]
        response = self._request("POST", "/extraction-task/", json=json_data)
        return [ExtractionTask.model_validate(item) for item in response.json()]

    def upsert_posts(self, posts: list[Post]) -> None:

        json_data = [post.model_dump(mode="json") for post in posts]
        self._request("POST", "/posts/", json=json_data)

    def upsert_accounts(self, accounts: list[Account]) -> None:

        json_data = [account.model_dump(mode="json") for account in accounts]
        self._request("POST", "/accounts/", json=json_data)
