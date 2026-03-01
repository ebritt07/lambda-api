from dataclasses import asdict
import base64
import json

from src.main.lambdas.common.dynamo_db_client import DynamoDbClient
from src.main.lambdas.common.dynamo_db_client import Table
from src.main.lambdas.common.dynamo_schema import Bike
from src.main.lambdas.common.auth import get_caller_sub
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.api_gateway_response import api_response

ddb = DynamoDbClient()
table = ddb.dynamodb.Table(Table.BIKES)
MAX_LIST_LIMIT = 100
DEFAULT_LIST_LIMIT = 25
LIST_PROJECTION_ATTRS = ("id", "make", "model", "style", "notes")


def _is_owner(item: dict, caller_sub: str) -> bool:
    return item.get("owner_id") == caller_sub


def _request_path(event: dict) -> str:
    return event.get("rawPath") or event.get("path") or ""


def _encode_next_token(last_evaluated_key: dict | None) -> str | None:
    if not last_evaluated_key:
        return None
    token_bytes = json.dumps(last_evaluated_key).encode("utf-8")
    return base64.urlsafe_b64encode(token_bytes).decode("utf-8")


def _decode_next_token(token: str | None) -> dict | None:
    if not token:
        return None
    try:
        token_bytes = base64.urlsafe_b64decode(token.encode("utf-8"))
        value = json.loads(token_bytes.decode("utf-8"))
    except Exception:
        raise ValueError("Invalid next_token")
    if not isinstance(value, dict):
        raise ValueError("Invalid next_token")
    return value


def _parse_list_limit(query_params: dict) -> int:
    raw_limit = query_params.get("limit")
    if raw_limit is None:
        return DEFAULT_LIST_LIMIT
    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        raise ValueError("Invalid limit")
    if limit < 1 or limit > MAX_LIST_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_LIST_LIMIT}")
    return limit


def _list_bikes(event: dict):
    query_params = event.get("queryStringParameters") or {}
    try:
        limit = _parse_list_limit(query_params)
        exclusive_start_key = _decode_next_token(query_params.get("next_token"))
    except ValueError as exc:
        return api_response({"message": str(exc)}, status_code=400)

    expression_attr_names = {f"#f{i}": attr for i, attr in enumerate(LIST_PROJECTION_ATTRS)}
    scan_kwargs = {
        "Limit": limit,
        "ProjectionExpression": ", ".join(expression_attr_names.keys()),
        "ExpressionAttributeNames": expression_attr_names,
    }
    if exclusive_start_key:
        scan_kwargs["ExclusiveStartKey"] = exclusive_start_key

    response = table.scan(**scan_kwargs)
    items = response.get("Items", [])
    returned_count = len(items)
    scanned_count = response.get("ScannedCount", 0)
    logger.info(
        "bike list scan limit=%s scanned_count=%s returned_count=%s",
        limit,
        scanned_count,
        returned_count,
    )
    return api_response(
        {
            "items": items,
            "next_token": _encode_next_token(response.get("LastEvaluatedKey")),
            "count": returned_count,
        }
    )


def handler(event, context):
    method = event["httpMethod"]
    path = _request_path(event)

    if method == "GET":
        if path.endswith("/bike/list"):
            return _list_bikes(event)

        query_params = event.get("queryStringParameters") or {}
        bike_id = query_params.get("id")
        if not bike_id:
            return api_response({"message": "Missing required query parameter: id"}, status_code=400)

        response = table.get_item(Key={
            'id': bike_id
        }
        )
        item = response.get('Item')
        if not item:
            return api_response({"message": "Bike not found"}, status_code=404)
        return api_response(item)

    if method == "PUT":
        caller_sub = get_caller_sub(event)
        if not caller_sub:
            return api_response({"message": "Unauthorized"}, status_code=401)

        bike_id = event["queryStringParameters"]["id"]
        response = table.get_item(Key={"id": bike_id})
        item = response.get("Item")
        if not item:
            return api_response({"message": "Bike not found"}, status_code=404)
        if not _is_owner(item, caller_sub):
            return api_response({"message": "Forbidden"}, status_code=403)

        body = json.loads(event["body"])
        bike_data = dict(body)
        bike_data["owner_id"] = caller_sub
        bike_data["id"] = bike_id
        bike = Bike(**bike_data)
        table.put_item(Item=asdict(bike))
        return api_response(bike)

    if method == "DELETE":
        caller_sub = get_caller_sub(event)
        if not caller_sub:
            return api_response({"message": "Unauthorized"}, status_code=401)

        bike_id = event["queryStringParameters"]["id"]
        response = table.get_item(Key={"id": bike_id})
        item = response.get("Item")
        if not item:
            return api_response({"message": "Bike not found"}, status_code=404)
        if not _is_owner(item, caller_sub):
            return api_response({"message": "Forbidden"}, status_code=403)

        table.delete_item(Key={"id": bike_id})
        logger.info(f"deleted bike id {bike_id}")
        return api_response(None, status_code=204)

    caller_sub = get_caller_sub(event)
    if not caller_sub:
        return api_response({"message": "Unauthorized"}, status_code=401)

    body = json.loads(event["body"])
    bike_data = dict(body)
    bike_data["owner_id"] = caller_sub
    bike = Bike(**bike_data)
    table.put_item(Item=asdict(bike))
    return api_response(bike)
