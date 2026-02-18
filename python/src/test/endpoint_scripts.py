#!/usr/bin/env python3
import os
import sys

import requests


def _resolve_endpoint() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    endpoint = os.getenv("LAMBDA_API_ENDPOINT")
    if endpoint:
        return endpoint
    print("Provide endpoint as argv[1] or set LAMBDA_API_ENDPOINT.", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    endpoint = _resolve_endpoint()
    response = requests.get(endpoint, timeout=30)
    print(f"GET {endpoint} -> {response.status_code}")
    print(response.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
