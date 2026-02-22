#!/usr/bin/env python3
import json
import os
import random
import time

import requests

from src.api_gateway_schema.external_schema import BikeDTO

BASE_URL = os.environ.get("BASE_URL", "https://api.ebritt07.click")
AUTH_URL = os.environ.get("AUTH_URL", "")
AUTH_USERNAME = os.environ.get("AUTH_USERNAME", "")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "")


def _extract_access_token(payload):
    for key in ("access_token", "id_token", "token"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value

    authentication_result = payload.get("AuthenticationResult")
    if isinstance(authentication_result, dict):
        for key in ("AccessToken", "IdToken"):
            value = authentication_result.get(key)
            if isinstance(value, str) and value:
                return value

    return None


def get_auth_token():
    if AUTH_TOKEN:
        return AUTH_TOKEN

    if not AUTH_URL:
        raise ValueError("Set AUTH_TOKEN or AUTH_URL for authenticated endpoint calls.")
    if not AUTH_USERNAME or not AUTH_PASSWORD:
        raise ValueError("Set AUTH_USERNAME and AUTH_PASSWORD for sign-in.")

    response = requests.post(
        AUTH_URL,
        json={"username": AUTH_USERNAME, "password": AUTH_PASSWORD},
        timeout=30,
    )
    response.raise_for_status()

    token = _extract_access_token(response.json())
    if not token:
        raise ValueError("Auth response did not include a supported token field.")
    return token


def auth_headers():
    return {"Authorization": f"Bearer {get_auth_token()}"}


def run_valid_call(method, id=1):
    request_start = time.perf_counter()

    if method == "GET":
        endpoint = f"{BASE_URL}/bike"
        endpoint += f"?id={id}"
        response = requests.get(endpoint, timeout=30)

    if method == "POST":
        endpoint = f"{BASE_URL}/bike/new"
        bike = BikeDTO(make="orbea", model="orca", style="FIXIE")
        response = requests.post(
            endpoint,
            json=bike.model_dump(),
            headers=auth_headers(),
            timeout=30,
        )

    if method == "PUT":
        endpoint = f"{BASE_URL}/bike"
        endpoint += f"?id={id}"
        bike = BikeDTO(make="orbea", model=f"orca {random.random()}", style="FIXIE")
        response = requests.put(
            endpoint,
            json=bike.model_dump(),
            headers=auth_headers(),
            timeout=30,
        )

    request_elapsed = time.perf_counter() - request_start
    print(f"{method} {endpoint} -> {response.status_code}")
    print(response.text)
    print(f"{method} took {request_elapsed:.3f}s")
    data = json.loads(response.text)
    return data

def run_invalid_call(method):
    request_start = time.perf_counter()
    if method == "GET":
        endpoint = f"{BASE_URL}/bike"
        response = requests.get(endpoint, timeout=30)
    if method == "POST":
        json = {"weird":2}
        endpoint = f"{BASE_URL}/bike/new"
        response = requests.post(endpoint, json=json, headers=auth_headers(), timeout=30)
    if method == "PUT":
        endpoint = f"{BASE_URL}/bike"
        json = {"weird":2}
        response = requests.put(endpoint, json=json, headers=auth_headers(), timeout=30)
    request_elapsed = time.perf_counter() - request_start
    print(f"{method} {endpoint} -> {response.status_code}")
    print(response.text)
    print(f"{method} took {request_elapsed:.3f}s")
    return response


if __name__ == "__main__":
    data = run_valid_call("POST")
    assert "id" in data, "POST response should contain id"
    bike_model = data["model"]
    assert bike_model.startswith("orca"), "POST response should contain correct model"
    bike_id = data["id"]
    data = run_valid_call("GET", id=bike_id)
    assert data["model"] == bike_model, "GET response should contain correct model"
    data = run_valid_call("PUT", id=bike_id)
    assert data["model"] != bike_model, "PUT response should update model"

    response = run_invalid_call("GET")
    assert response.status_code == 400, "GET without id should return 400"
    response = run_invalid_call("POST")
    assert response.status_code == 400, "POST with invalid body should return 400"
