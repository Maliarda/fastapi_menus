import aioredis
from aioredis import Redis

from app.core.config import settings


async def get_cache() -> Redis:
    redis = aioredis.from_url(
        settings.redis_url,
        max_connections=10,
        encoding='utf8',
        decode_responses=True,
    )
    return redis


async def cache_init() -> None:
    r = await get_cache()
    await r.flushall()
