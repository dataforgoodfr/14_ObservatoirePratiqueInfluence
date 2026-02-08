import logging

from fastapi import HTTPException

from app.models import Influencer
from app.db import pool

LOGGER = logging.getLogger(__name__)


async def get_influencer_accounts(
    username: str,
) -> Influencer:
    fetch_assays = """
        SELECT
            uid
            , username
        FROM
            v1.influencer
    """
    async with pool.PGPool.get_connection() as conn:
        try:
            row = await conn.fetchrow(fetch_assays)
            return Influencer(
                uid=row[0],
                username=row[1],
            )
        except TypeError as e:
            raise HTTPException(
                status_code=404, detail=f"Influencer {username} not found"
            ) from e
        except Exception as e:
            LOGGER.exception(f"Error fetching influencer account {username}")
            raise e
