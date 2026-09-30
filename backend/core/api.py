import logging

from django.db import connection
from django.http import HttpRequest
from ninja import NinjaAPI, Schema, Status

from core.redis_client import get_redis

logger = logging.getLogger(__name__)

api = NinjaAPI(title="DocWise", version="0.1.0")


class Health(Schema):
    status: str


class Ready(Schema):
    db: bool
    redis: bool


def _db_ok() -> bool:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as exc:
        logger.warning("event=ready_check_failed check=db error=%s", type(exc).__name__)
        return False


def _redis_ok() -> bool:
    try:
        return bool(get_redis().ping())
    except Exception as exc:
        logger.warning("event=ready_check_failed check=redis error=%s", type(exc).__name__)
        return False


@api.get("/health", response=Health)
def health(request: HttpRequest) -> dict[str, str]:
    """Liveness only. Touches no dependencies (used as the Lambda readiness check)."""
    return {"status": "ok"}


@api.get("/ready", response={200: Ready, 503: Ready})
def ready(request: HttpRequest) -> Status[dict[str, bool]]:
    """Checks that Postgres and Redis are reachable."""
    checks = {"db": _db_ok(), "redis": _redis_ok()}
    return Status(200 if all(checks.values()) else 503, checks)
