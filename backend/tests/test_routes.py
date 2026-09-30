import pytest
from django.urls import Resolver404, resolve


def test_openapi_docs_render(client):
    assert client.get("/api/docs").status_code == 200

    paths = client.get("/api/openapi.json").json()["paths"]
    assert {"/api/health", "/api/ready"} <= set(paths)


def test_admin_is_not_routed_outside_debug(settings):
    # pytest-django runs with DEBUG=False, which is also the production value.
    assert settings.DEBUG is False
    with pytest.raises(Resolver404):
        resolve("/admin/")
