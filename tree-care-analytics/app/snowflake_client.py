import asyncio
import time
from typing import Any

from app.config import Settings

_CACHE: dict[str, tuple[float, Any]] = {}


class SnowflakeUnavailable(RuntimeError):
    pass


def _connect(settings: Settings):
    import snowflake.connector

    return snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=settings.snowflake_schema,
        role=settings.snowflake_role,
        client_session_keep_alive=True,
    )


def _run(settings: Settings, sql: str, params: tuple | None = None) -> list[dict]:
    conn = _connect(settings)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            columns = [c[0].lower() for c in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()


async def query(
    settings: Settings,
    sql: str,
    params: tuple | None = None,
    cache_ttl: int = 300,
) -> list[dict]:
    """Run an analytical query against Snowflake.

    A cold virtual warehouse can take seconds to resume and every statement is
    billed, so results are cached and the blocking driver is pushed to a worker
    thread. Never put an uncached call to this on a user-facing request path.
    """
    if not settings.snowflake_configured:
        raise SnowflakeUnavailable(
            "Snowflake credentials are not set; see README Layer 3."
        )

    key = f"{sql}|{params}"
    hit = _CACHE.get(key)
    now = time.monotonic()
    if hit and now - hit[0] < cache_ttl:
        return hit[1]

    rows = await asyncio.to_thread(_run, settings, sql, params)
    _CACHE[key] = (now, rows)
    return rows
