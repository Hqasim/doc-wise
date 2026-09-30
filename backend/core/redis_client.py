from functools import cache

import redis
from django.conf import settings


@cache
def get_redis() -> redis.Redis:
    """Return the shared Redis client (one connection pool per process)."""
    return redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=settings.REDIS_TIMEOUT_SECONDS,
        socket_timeout=settings.REDIS_TIMEOUT_SECONDS,
    )
