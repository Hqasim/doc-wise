import pytest

from core import api


def test_health_returns_ok_without_touching_dependencies(client, monkeypatch):
    # No django_db mark: pytest-django raises if the view touches the database.
    def fail():
        pytest.fail("/health must not touch Redis")

    monkeypatch.setattr(api, "get_redis", fail)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
