#!/usr/bin/env python3
import os
import random
import sys
import time

import requests

from src.api_gateway_schema.external_schema import BikeDTO

def _resolve_method() -> str:
    for i in ["GET", "POST", "PUT"]:
        if input(i + "? (y/n)") == "y":
            return(i)
    return ("GET")

def run() -> int:
    method = _resolve_method()
    id = input("ID:")
    request_start = time.perf_counter()

    if method == "GET":
        endpoint = "https://3gkge57tg1.execute-api.us-east-1.amazonaws.com/bike"
        endpoint += f"?id={id}"
        response = requests.get(endpoint, timeout=30)

    if method == "POST":
        endpoint = "https://3gkge57tg1.execute-api.us-east-1.amazonaws.com/bike/new"
        bike = BikeDTO(make="orbea", model="orca", )
        response = requests.post(endpoint, json=bike.model_dump(), timeout=30)

    if method == "PUT":
        endpoint = "https://3gkge57tg1.execute-api.us-east-1.amazonaws.com/bike"
        endpoint += f"?id={id}"
        bike = BikeDTO(make="orbea", model="orca "+str(random.random()), style="FIXIE")
        response = requests.put(endpoint, json=bike.model_dump(), timeout=30)

    request_elapsed = time.perf_counter() - request_start
    print(f"{method} {endpoint} -> {response.status_code}")
    print(response.text)
    print(f"{method} took {request_elapsed:.3f}s")


if __name__ == "__main__":
    run()
