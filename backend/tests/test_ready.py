import pytest

from core.redis_client import get_redis


@pytest.fixture(autouse=True)
def fresh_redis_client():
    get_redis.cache_clear()
    yield
    get_redis.cache_clear()


@pytest.mark.django_db
def test_ready_returns_200_when_db_and_redis_are_up(client):
    response = client.get("/api/ready")

    assert response.status_code == 200
    assert response.json() == {"db": True, "redis": True}


@pytest.mark.django_db
def test_ready_returns_503_when_redis_is_unreachable(client, settings):
    settings.REDIS_URL = "redis://127.0.0.1:1/0"
    settings.REDIS_TIMEOUT_SECONDS = 0.5

    response = client.get("/api/ready")

    assert response.status_code == 503
    assert response.json() == {"db": True, "redis": False}
