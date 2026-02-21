#!/usr/bin/env python3
import json
import os
import random
import time
import requests

from src.api_gateway_schema.external_schema import BikeDTO

BASE_URL = os.environ["LAMBDA_BASE_URL"]

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

if __name__ == "__main__":
    data = run_valid_call("POST")
    if "id" in data:
        bike_id = data["id"]
        run_valid_call("GET", id=bike_id)
        run_valid_call("PUT", id=bike_id)

    run_invalid_call("GET")
    run_invalid_call("POST")

