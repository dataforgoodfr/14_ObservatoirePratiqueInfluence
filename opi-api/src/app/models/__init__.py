"""OPI API models."""

from app.models.socialnetwork import Account, Post, SocialNetwork
from app.models.task import (
    DetailedStats,
    ExtractionTask,
    ExtractionTaskResponse,
    ExtractionTaskStatsResponse,
    ExtractionTaskStatus,
    ExtractionTaskType,
    MarkTaskFailedPayload,
    NetworkCount,
    RecycleExpiredTasksResponse,
    RecycleFailedTasksResponse,
    StatusCount,
    TaskTypeCount,
)

__all__ = [
    "Account",
    "DetailedStats",
    "ExtractionTask",
    "ExtractionTaskResponse",
    "ExtractionTaskStatsResponse",
    "ExtractionTaskStatus",
    "ExtractionTaskType",
    "MarkTaskFailedPayload",
    "NetworkCount",
    "Post",
    "RecycleExpiredTasksResponse",
    "RecycleFailedTasksResponse",
    "SocialNetwork",
    "StatusCount",
    "TaskTypeCount",
]
