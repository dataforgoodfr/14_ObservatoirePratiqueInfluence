import json
import logging
import uuid
from http import HTTPStatus

import fastapi

from app._auth import validate_api_key
from app.db import pool
from app.models import ExtractionTask, ExtractionTaskResponse, ExtractionTaskStatus, SocialNetwork

LOGGER = logging.getLogger(__name__)
API_KEY = fastapi.Depends(validate_api_key)


async def acquire_available_task(
    api_key: str = API_KEY,
    social_network: SocialNetwork | None = None,
) -> ExtractionTaskResponse:
    get_task = """
        UPDATE v1.extraction_task
        SET status = 'ACQUIRED', visible_at = NOW() + INTERVAL '15 minutes'
        WHERE uid = (
            SELECT uid
            FROM v1.extraction_task
            WHERE status = 'AVAILABLE'
            AND ($1::text IS NULL OR social_network = $1::text)
            ORDER BY
                -- Make extract-post-details higher priority
                case type when 'extract-post-details' then 0 else 1 end ASC,
                created_at ASC
            LIMIT 1
        )
        RETURNING uid
            , social_network
            , type
            , config
            , visible_at
        ;
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            row = await conn.fetchrow(get_task, social_network.value if social_network else None)

            if row:
                return ExtractionTaskResponse(
                    task_uid=row[0],
                    social_network=row[1],
                    type=row[2],
                    task_config=json.loads(row[3]),
                    visible_at=row[4],
                )
            return ExtractionTaskResponse(error="no-task-available")
        except Exception:
            LOGGER.exception("Error getting task")
            raise


async def update_task(
    task_uid: uuid.UUID,
    status: ExtractionTaskStatus,
    api_key: str = API_KEY,
) -> fastapi.Response:
    update_task = """
        UPDATE v1.extraction_task
        SET status = $2
            , visible_at = NULL
        WHERE uid = $1
            AND visible_at > NOW()
        ;
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            await conn.execute(update_task, task_uid, status)
            return fastapi.Response(status_code=HTTPStatus.NO_CONTENT)

        except Exception:
            message = f"Error updating task {task_uid}"
            LOGGER.exception(message)
            raise


async def register_tasks(
    extraction_tasks: list[ExtractionTask],
    api_key: str = API_KEY,
) -> list[ExtractionTask]:
    register_tasks = """
        INSERT INTO v1.extraction_task (
            social_network
            , type
            , config
            , status
        )
        (
            SELECT input.social_network
                , input.type
                , input.config
                , input.status
            FROM unnest($1::"v1"."extraction_task"[]) AS input
        )
        RETURNING
            uid
            , created_at
            , type
            , config
            , social_network
            , status
            , visible_at
            , error
    """

    task_list = [
        (
            None,
            None,
            task.type,
            task.task_config.model_dump_json(),
            task.social_network,
            ExtractionTaskStatus.AVAILABLE,
            None,
            None,
        )
        for task in extraction_tasks
    ]

    async with pool.PGPool.get_connection() as conn:
        try:
            rows = await conn.fetch(register_tasks, task_list)
            return [
                ExtractionTask(
                    uid=row[0],
                    type=row[2],
                    task_config=json.loads(row[3]),
                    social_network=row[4],
                    status=row[5],
                    visible_at=row[6],
                    error=row[7],
                )
                for row in rows
            ]
        except Exception:
            LOGGER.exception("Error inserting tasks")
            raise
