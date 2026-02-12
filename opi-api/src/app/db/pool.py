# noqa: D100

from __future__ import annotations

import contextlib
import logging
import os
from collections.abc import AsyncIterator

import asyncpg

logger = logging.getLogger("uvicorn")

DSN: str = (
    os.getenv("POSTGRES_DSN") or "postgresql://postgres:postgres@localhost:5432/opidb"
)
if "application_name" not in DSN:
    DSN += "&application_name=opi-api"

ASYNCPG_MIN_POOL_SIZE: int = int(os.getenv("ASYNCPG_MIN_POOL_SIZE", "1"))
ASYNCPG_MAX_POOL_SIZE: int = int(os.getenv("ASYNCPG_MAX_POOL_SIZE", "1"))


class PGPool:
    """Postgresql connection pool convenience class."""

    _pool: asyncpg.Pool | None = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool | None:
        """Get a postgres connection pool."""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=DSN,
                min_size=ASYNCPG_MIN_POOL_SIZE,
                max_size=ASYNCPG_MAX_POOL_SIZE,
                max_inactive_connection_lifetime=300,
                command_timeout=300,
            )

        return cls._pool

    @classmethod
    @contextlib.asynccontextmanager
    async def get_connection(cls) -> AsyncIterator:
        """Get a connection from the connection pool."""
        pool = await cls.get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                yield conn

    @classmethod
    async def close_connection(cls) -> None:
        """Close the connection pool."""
        if cls._pool is not None:
            logger.info("Closing connection pool")
            await cls._pool.close()
        else:
            logger.info("Connection pool already closed")
