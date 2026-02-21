import json

from src.main.lambdas.common.api_gateway_response import api_response
from src.main.lambdas.common.dynamo_schema import Bike


def test_api_response_wraps_body_and_status():
    payload = {"ok": True, "count": 2}
    response = api_response(payload, status_code=201)

    assert response["statusCode"] == 201
    assert response["headers"]["content-type"] == "application/json"
    assert json.loads(response["body"]) == payload


def test_api_response_normalizes_dataclass_body():
    bike = Bike(make="Orbea", model="Terra", style="ROAD", notes="test build")

    response = api_response(bike)
    body = json.loads(response["body"])

    assert body["make"] == bike.make
    assert body["model"] == bike.model
    assert body["style"] == bike.style
    assert body["notes"] == bike.notes
    assert body["id"] == bike.id


def test_api_response_merges_headers_with_overrides():
    response = api_response({"ok": True}, headers={"x-trace": "1", "content-type": "text/plain"})

    assert response["headers"]["x-trace"] == "1"
    assert response["headers"]["content-type"] == "text/plain"


def test_api_response_serializes_unknown_objects_with_str():
    class Something:
        def __str__(self) -> str:
            return "<something>"

    response = api_response({"value": Something()})

    assert json.loads(response["body"]) == {"value": "<something>"}
