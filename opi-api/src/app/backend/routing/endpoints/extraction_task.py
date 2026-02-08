import fastapi
import logging
import uuid
import json

from http import HTTPStatus

from app.models import ExtractionTask, ExtractionTaskResponse, ExtractionTaskStatus
from app.db import pool

LOGGER = logging.getLogger(__name__)


async def acquire_available_task() -> ExtractionTaskResponse:
    get_task = """
        UPDATE v1.extraction_task
        SET status = 'ACQUIRED', visible_until = NOW() + INTERVAL '15 minutes'
        WHERE uid = (
            SELECT uid
            FROM v1.extraction_task
            WHERE status = 'AVAILABLE'
            ORDER BY created_at ASC
            LIMIT 1
        )
        RETURNING uid
            , social_network
            , type
            , config
            , visible_until
            , error
        ;
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            row = await conn.fetchrow(get_task)

            if row:
                return ExtractionTaskResponse(
                    task_uid=row[0],
                    social_network=row[1],
                    type=row[2],
                    task_config=json.loads(row[3]),
                    visible_until=row[4],
                )
            else:
                return ExtractionTaskResponse(error="no-task-available")
        except Exception as e:
            LOGGER.exception("Error getting task")
            raise e


async def update_task(task_uid: uuid.UUID, status: ExtractionTaskStatus) -> None:
    update_task = """
        UPDATE v1.extraction_task
        SET status = $2
            , visible_until = NULL
        WHERE uid = $1
            AND visible_until > NOW()
        ;
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            await conn.execute(update_task, task_uid, status)
            return fastapi.Response(status_code=HTTPStatus.NO_CONTENT)

        except Exception as e:
            LOGGER.exception(f"Error updating task {task_uid}")
            raise e


async def register_tasks(
    extraction_tasks: list[ExtractionTask],
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
            , visible_until
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
                    created_at=row[1],
                    type=row[2],
                    task_config=json.loads(row[3]),
                    social_network=row[4],
                    status=row[5],
                    visible_until=row[6],
                    error=row[7],
                )
                for row in rows
            ]
        except Exception as e:
            LOGGER.exception("Error inserting tasks")
            raise e
