import json
import logging
import uuid
from http import HTTPStatus

import fastapi

from app._auth import validate_api_key
from app.db import pool
from app.models import (
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
    SocialNetwork,
    StatusCount,
    TaskTypeCount,
)

LOGGER = logging.getLogger(__name__)
API_KEY = fastapi.Depends(validate_api_key)


async def acquire_available_task(
    api_key: str = API_KEY,
    social_network: SocialNetwork | None = None,
) -> ExtractionTaskResponse:
    get_task = """
        UPDATE v1.extraction_task
        SET status = 'ACQUIRED', visible_at = NOW() + INTERVAL '120 minutes'
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


async def mark_completed(
    task_uid: uuid.UUID,
    api_key: str = API_KEY,
) -> fastapi.Response:
    update_task = """
        UPDATE v1.extraction_task
        SET status = 'COMPLETED'
            , visible_at = NULL
        WHERE uid = $1
            AND visible_at > NOW()
            AND status = 'ACQUIRED'
        ;
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            await conn.execute(update_task, task_uid)
            return fastapi.Response(status_code=HTTPStatus.NO_CONTENT)

        except Exception:
            message = f"Error updating task {task_uid}"
            LOGGER.exception(message)
            raise


async def mark_failed(
    task_uid: uuid.UUID,
    payload: MarkTaskFailedPayload,
    api_key: str = API_KEY,
) -> fastapi.Response:
    update_task = """
        UPDATE v1.extraction_task
        SET status = 'FAILED'
            , visible_at = NULL
            , error = $2
        WHERE uid = $1
            AND visible_at > NOW()
            AND status = 'ACQUIRED'
        ;
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            await conn.execute(update_task, task_uid, ExtractionTaskStatus.FAILED, payload.error)
            return fastapi.Response(status_code=HTTPStatus.NO_CONTENT)

        except Exception:
            message = f"Error updating task {task_uid}"
            LOGGER.exception(message)
            raise


async def recycle_failed_tasks(
    api_key: str = API_KEY,
) -> RecycleFailedTasksResponse:
    """Recycle all failed tasks back to available status.

    This endpoint finds all tasks with status 'FAILED' and updates them to
    'AVAILABLE' status, making them available for acquisition again.
    The visible_at is set to NULL so they become immediately available.
    The error field is also cleared.
    """
    recycle_tasks = """
        UPDATE v1.extraction_task
        SET status = 'AVAILABLE'
            , visible_at = NULL
            , error = NULL
        WHERE status = 'FAILED'
        RETURNING uid
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            rows = await conn.fetch(recycle_tasks)
            return RecycleFailedTasksResponse(recycled_count=len(rows))
        except Exception:
            LOGGER.exception("Error recycling failed tasks")
            raise


async def recycle_expired_tasks(
    api_key: str = API_KEY,
) -> RecycleExpiredTasksResponse:
    """Recycle all acquired tasks that have passed their acquisition limit.

    This endpoint finds all tasks with status 'ACQUIRED' where visible_at < NOW()
    (meaning the acquisition time has expired) and updates them to 'AVAILABLE' status,
    making them available for acquisition again. The visible_at is set to NULL so they
    become immediately available.
    """
    recycle_tasks = """
        UPDATE v1.extraction_task
        SET status = 'AVAILABLE'
            , visible_at = NULL
        WHERE status = 'ACQUIRED'
            AND visible_at < NOW()
        RETURNING uid
    """

    async with pool.PGPool.get_connection() as conn:
        try:
            rows = await conn.fetch(recycle_tasks)
            return RecycleExpiredTasksResponse(recycled_count=len(rows))
        except Exception:
            LOGGER.exception("Error recycling expired tasks")
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


async def get_extraction_task_stats(
    api_key: str = API_KEY,
    social_network: SocialNetwork | None = None,
    account_id: str | None = None,
    task_type: ExtractionTaskType | None = None,
) -> ExtractionTaskStatsResponse:
    """Get statistics on extraction tasks.

    This endpoint provides global and detailed statistics on extraction tasks,
    with optional filters for social network, account ID, and task type.

    Global stats include:
    - Count per extended status (AVAILABLE, ACQUIRED_VALID, ACQUIRED_EXPIRED, COMPLETED, FAILED)
    - Count per task type
    - Count per network

    Detailed stats include:
    - Counts for each combination of task type, network, and extended status
    """
    # Build the WHERE clause for filters
    where_clauses = []
    params = []
    param_index = 1

    if social_network:
        where_clauses.append(f"social_network = ${param_index}")
        params.append(social_network.value)
        param_index += 1

    if account_id:
        where_clauses.append(f"config->>'account_id' = ${param_index}")
        params.append(account_id)
        param_index += 1

    if task_type:
        where_clauses.append(f"type = ${param_index}")
        params.append(task_type.value)
        param_index += 1

    where_clause = " AND ".join(where_clauses) if where_clauses else "TRUE"

    # Query for global stats - count per extended status
    status_query = f"""
        SELECT
            CASE
                WHEN status = 'ACQUIRED' AND visible_at > NOW() THEN 'ACQUIRED_VALID'
                WHEN status = 'ACQUIRED' AND visible_at <= NOW() THEN 'ACQUIRED_EXPIRED'
                ELSE status
            END AS extended_status,
            COUNT(*) AS count
        FROM v1.extraction_task
        WHERE {where_clause}
        GROUP BY extended_status
        ORDER BY extended_status
    """  # noqa: S608

    # Query for global stats - count per task type
    type_query = f"""
        SELECT type, COUNT(*) AS count
        FROM v1.extraction_task
        WHERE {where_clause}
        GROUP BY type
        ORDER BY type
    """  # noqa: S608 - where_clause is safe

    # Query for global stats - count per network
    network_query = f"""
        SELECT social_network, COUNT(*) AS count
        FROM v1.extraction_task
        WHERE {where_clause}
        GROUP BY social_network
        ORDER BY social_network
    """  # noqa: S608 - where_clause is safe

    # Query for detailed stats - count per combination of type, network, and extended status
    detailed_query = f"""
        SELECT
            type,
            social_network,
            CASE
                WHEN status = 'ACQUIRED' AND visible_at > NOW() THEN 'ACQUIRED_VALID'
                WHEN status = 'ACQUIRED' AND visible_at <= NOW() THEN 'ACQUIRED_EXPIRED'
                ELSE status
            END AS extended_status,
            COUNT(*) AS count
        FROM v1.extraction_task
        WHERE {where_clause}
        GROUP BY type, social_network, extended_status
        ORDER BY type, social_network, extended_status
    """  # noqa: S608 - where_clause is safe

    async with pool.PGPool.get_connection() as conn:
        try:
            # Execute all queries
            status_rows = await conn.fetch(status_query, *params)
            type_rows = await conn.fetch(type_query, *params)
            network_rows = await conn.fetch(network_query, *params)
            detailed_rows = await conn.fetch(detailed_query, *params)

            # Build global stats
            global_stats = {
                "status_counts": [
                    StatusCount(status=row[0], count=row[1]).model_dump() for row in status_rows
                ],
                "type_counts": [
                    TaskTypeCount(type=row[0], count=row[1]).model_dump() for row in type_rows
                ],
                "network_counts": [
                    NetworkCount(social_network=row[0], count=row[1]).model_dump()
                    for row in network_rows
                ],
            }

            # Build detailed stats
            detailed_stats = [
                DetailedStats(
                    type=row[0],
                    social_network=row[1],
                    status=row[2],
                    count=row[3],
                )
                for row in detailed_rows
            ]

            return ExtractionTaskStatsResponse(
                global_stats=global_stats,
                detailed_stats=detailed_stats,
            )
        except Exception:
            LOGGER.exception("Error getting extraction task stats")
            raise
