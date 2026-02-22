#!/usr/bin/env python3
import json
import os
import random
import time
import requests

from src.api_gateway_schema.external_schema import BikeDTO

BASE_URL = os.environ.get("BASE_URL", "https://api.ebritt07.click")

def run_valid_call(method, id=1):
    request_start = time.perf_counter()

    if method == "GET":
        endpoint = f"{BASE_URL}/bike"
        endpoint += f"?id={id}"
        response = requests.get(endpoint, timeout=30)

    if method == "POST":
        endpoint = f"{BASE_URL}/bike/new"
        bike = BikeDTO(make="orbea", model="orca", style="FIXIE")
        response = requests.post(endpoint, json=bike.model_dump(), timeout=30)

    if method == "PUT":
        endpoint = f"{BASE_URL}/bike"
        endpoint += f"?id={id}"
        bike = BikeDTO(make="orbea", model="orca "+str(random.random()), style="FIXIE")
        response = requests.put(endpoint, json=bike.model_dump(), timeout=30)

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
    assert response.status_code == 400, "GET without id should return 400"
    run_invalid_call("POST")
    assert response.status_code == 400, "POST with invalid body should return 400"

