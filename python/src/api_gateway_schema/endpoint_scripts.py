#!/usr/bin/env python3
import json
import os
import random
import time
import requests

from src.api_gateway_schema.external_schema import BikeDTO

env_input = input("Use local env? (y/n): ")

ENV = "local" if env_input.strip().lower() =="y" else "dev"
BASE_URL = "http://localhost:8000" if ENV == "local" else "https://api.ebritt07.click"
MOCK_TOKEN =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." + \
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpva" + \
        "G4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNj" + \
        "IzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"

def _auth_header():

    token = MOCK_TOKEN
    return {"Authorization": f"Bearer {token}"}

def run_valid_call(method, id=1):
    request_start = time.perf_counter()

    if method == "GET":
        endpoint = f"{BASE_URL}/bike"
        endpoint += f"?id={id}"
        response = requests.get(endpoint, timeout=30)

    if method == "POST":
        endpoint = f"{BASE_URL}/bike/new"
        bike = BikeDTO(make="orbea", model="orca", style="FIXIE")
        response = requests.post(endpoint, json=bike.model_dump(), headers=_auth_header(), timeout=30)

    if method == "PUT":
        endpoint = f"{BASE_URL}/bike"
        endpoint += f"?id={id}"
        bike = BikeDTO(make="orbea", model="orca "+str(random.random()), style="FIXIE")
        response = requests.put(endpoint, json=bike.model_dump(), headers=_auth_header(), timeout=30)

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
        response = requests.post(endpoint, json=json, timeout=30)
    if method == "PUT":
        endpoint = f"{BASE_URL}/bike"
        json = {"weird":2}
        response = requests.put(endpoint, json=json, timeout=30)        
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
    assert 400 <= response.status_code < 500, "GET without id should return 4xx"
    run_invalid_call("POST")
    response = run_invalid_call("POST")
    assert 400 <= response.status_code < 500, "POST with invalid body should return 4xx"

