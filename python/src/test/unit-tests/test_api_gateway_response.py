import json

from src.main.lambdas.common.api_gateway_response import api_response


def test_api_response_wraps_body_and_status():
    payload = {"ok": True, "count": 2}
    response = api_response(payload, status_code=201)

    assert response["statusCode"] == 201
    assert response["headers"]["content-type"] == "application/json"
    assert json.loads(response["body"]) == payload
