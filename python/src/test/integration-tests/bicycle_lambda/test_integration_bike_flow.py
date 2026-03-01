import os
import base64
import json

os.environ["ENV"] = "LOCAL"

import pytest 
from fastapi.testclient import TestClient

from src.test.main import app
from src.test.test_util.dynamodb import LocalDynamoManager
from src.main.lambdas.common.dynamo_db_client import DynamoDbClient, Table


def _is_codex_env() -> bool:
    return any(
        os.getenv(key)
        for key in (
            "CODEX_CI",
            "CODEX_SANDBOX",
            "CODEX_THREAD_ID",
        )
    )



def _bearer_headers(sub: str) -> dict[str, str]:
    payload = {"sub": sub}
    payload_bytes = json.dumps(payload).encode("utf-8")
    payload_segment = (
        base64.urlsafe_b64encode(payload_bytes).decode("utf-8").rstrip("=")
    )
    token = f"header.{payload_segment}.signature"
    return {"Authorization": f"Bearer {token}"}


def _clear_bikes_table():
    ddb = DynamoDbClient()
    bike_table = ddb.dynamodb.Table(Table.BIKES)
    scan_response = bike_table.scan(ProjectionExpression="id")
    for item in scan_response.get("Items", []):
        bike_table.delete_item(Key={"id": item["id"]})


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


@pytest.mark.skipif(
    _is_codex_env(),
    reason="DynamoDB Local cannot bind sockets in Codex environment",
)
def test_bike_crud_flow_in_order(client):
    create_payload = {
        "make": "Orbea",
        "model": "Terra",
        "style": "ROAD",
        "notes": "first build",
    }

    response = client.post(
        "/bike/new",
        json=create_payload,
        headers=_bearer_headers("user-1"),
    )
    assert response.status_code == 200
    created_bike = response.json()
    assert "id" in created_bike
    assert created_bike["owner_id"] == "user-1"
    bike_id = created_bike["id"]

    response = client.get("/bike", params={"id": bike_id})
    assert response.status_code == 200
    fetched_bike = response.json()
    assert fetched_bike["id"] == bike_id
    assert fetched_bike["owner_id"] == "user-1"

    update_payload = {
        "make": "Orbea",
        "model": "Terra M31e",
        "style": "ROAD",
        "notes": "updated build",
    }

    response = client.put(
        "/bike",
        params={"id": bike_id},
        json=update_payload,
        headers=_bearer_headers("user-1"),
    )
    assert response.status_code == 200
    updated_bike = response.json()
    assert updated_bike["id"] == bike_id
    assert updated_bike["owner_id"] == "user-1"
    assert updated_bike["model"] == update_payload["model"]

    response = client.get("/bike", params={"id": bike_id})
    assert response.status_code == 200
    fetched_after_update = response.json()
    assert fetched_after_update["model"] == update_payload["model"]
    assert fetched_after_update["owner_id"] == "user-1"

    response = client.delete(
        "/bike",
        params={"id": bike_id},
        headers=_bearer_headers("user-1"),
    )
    assert response.status_code == 204


@pytest.mark.skipif(
    _is_codex_env(),
    reason="DynamoDB Local cannot bind sockets in Codex environment",
)
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

    response = client.put(
        "/bike",
        params={"id": missing_id},
        json=update_payload,
        headers=_bearer_headers("user-1"),
    )
    assert response.status_code == 404


@pytest.mark.skipif(
    _is_codex_env(),
    reason="DynamoDB Local cannot bind sockets in Codex environment",
)
def test_bike_update_delete_forbidden_for_non_owner(client):
    create_payload = {
        "make": "Orbea",
        "model": "Terra",
        "style": "ROAD",
        "notes": "owner check",
    }

    create_response = client.post(
        "/bike/new",
        json=create_payload,
        headers=_bearer_headers("owner-user"),
    )
    assert create_response.status_code == 200
    bike_id = create_response.json()["id"]

    update_payload = {
        "make": "Orbea",
        "model": "Terra M31e",
        "style": "ROAD",
        "notes": "wrong user",
    }

    update_response = client.put(
        "/bike",
        params={"id": bike_id},
        json=update_payload,
        headers=_bearer_headers("other-user"),
    )
    assert update_response.status_code == 403

    delete_response = client.delete(
        "/bike",
        params={"id": bike_id},
        headers=_bearer_headers("other-user"),
    )
    assert delete_response.status_code == 403


@pytest.mark.skipif(
    _is_codex_env(),
    reason="DynamoDB Local cannot bind sockets in Codex environment",
)
def test_bike_list_scan_paginates_and_hides_owner_id(client):
    _clear_bikes_table()

    created_ids = set()
    for i in range(3):
        response = client.post(
            "/bike/new",
            json={
                "make": f"ListTest-{i}",
                "model": f"Model-{i}",
                "style": "ROAD",
                "notes": f"list-notes-{i}",
            },
            headers=_bearer_headers(f"user-{i}"),
        )
        assert response.status_code == 200
        created_ids.add(response.json()["id"])

    page_1 = client.get("/bike/list", params={"limit": 2})
    assert page_1.status_code == 200
    page_1_data = page_1.json()
    assert page_1_data["count"] == 2
    assert len(page_1_data["items"]) == 2
    assert page_1_data["next_token"]
    for item in page_1_data["items"]:
        assert "owner_id" not in item

    page_2 = client.get(
        "/bike/list",
        params={"limit": 2, "next_token": page_1_data["next_token"]},
    )
    assert page_2.status_code == 200
    page_2_data = page_2.json()
    assert page_2_data["count"] == 1
    assert len(page_2_data["items"]) == 1
    assert page_2_data["next_token"] is None
    for item in page_2_data["items"]:
        assert "owner_id" not in item

    listed_ids = {item["id"] for item in page_1_data["items"] + page_2_data["items"]}
    assert listed_ids == created_ids


@pytest.mark.skipif(
    _is_codex_env(),
    reason="DynamoDB Local cannot bind sockets in Codex environment",
)
def test_bike_list_invalid_next_token_returns_400(client):
    response = client.get("/bike/list", params={"next_token": "not-a-valid-token"})
    assert response.status_code == 400
