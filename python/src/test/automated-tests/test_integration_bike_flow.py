import os

os.environ["ENV"] = "LOCAL"

import pytest
from fastapi.testclient import TestClient

from src.test.main import app
from src.test.test_util.dynamodb import LocalDynamoManager


def _is_codex_env() -> bool:
    return any(
        os.getenv(key)
        for key in (
            "CODEX_CI",
            "CODEX_SANDBOX",
            "CODEX_THREAD_ID",
        )
    )


@pytest.fixture(scope="session")
def local_dynamo_manager():
    manager = LocalDynamoManager()
    manager.start_local_dynamo()
    try:
        yield manager
    finally:
        manager.terminate_local_dynamo()


@pytest.fixture()
def client(local_dynamo_manager):
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.skipif(_is_codex_env(), reason="DynamoDB Local cannot bind sockets in Codex environment")
def test_bike_crud_flow_in_order(client):
    create_payload = {
        "make": "Orbea",
        "model": "Terra",
        "style": "ROAD",
        "notes": "first build",
    }

    response = client.post("/bike/new", json=create_payload)
    assert response.status_code == 200
    created_bike = response.json()
    assert "id" in created_bike
    bike_id = created_bike["id"]

    response = client.get("/bike", params={"id": bike_id})
    assert response.status_code == 200
    fetched_bike = response.json()
    assert fetched_bike["id"] == bike_id

    update_payload = {
        "make": "Orbea",
        "model": "Terra M31e",
        "style": "ROAD",
        "notes": "updated build",
    }

    response = client.put(f"/bike/{bike_id}", json=update_payload)
    assert response.status_code == 200
    updated_bike = response.json()
    assert updated_bike["id"] == bike_id
    assert updated_bike["model"] == update_payload["model"]

    response = client.get("/bike", params={"id": bike_id})
    assert response.status_code == 200
    fetched_after_update = response.json()
    assert fetched_after_update["model"] == update_payload["model"]

    response = client.delete(f"/bike/{bike_id}")
    assert response.status_code == 204


@pytest.mark.skipif(_is_codex_env(), reason="DynamoDB Local cannot bind sockets in Codex environment")
def test_bike_get_put_missing_returns_404(client):
    missing_id = "missing-id-123"

    response = client.get("/bike", params={"id": missing_id})
    assert response.status_code == 404

    update_payload = {
        "make": "Orbea",
        "model": "Terra",
        "style": "ROAD",
        "notes": "should fail",
    }

    response = client.put(f"/bike/{missing_id}", json=update_payload)
    assert response.status_code == 404
