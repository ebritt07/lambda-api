import json
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Optional

_CORS_ORIGIN_HEADER = {"Access-Control-Allow-Origin": "*"}


def _normalize_body(body: Any) -> Any:
    if is_dataclass(body):
        return asdict(body)
    return body


def api_response(
        body: Any,
        *,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        is_base64_encoded: bool = False,
) -> Dict[str, Any]:
    safe_body = _normalize_body(body)
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
            **_CORS_ORIGIN_HEADER,
            **(headers or {}),
        },
        "body": json.dumps(safe_body, default=str),
        "isBase64Encoded": is_base64_encoded,
    }
