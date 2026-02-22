from dataclasses import asdict
import json

from src.main.lambdas.common.dynamo_db_client import DynamoDbClient
from src.main.lambdas.common.dynamo_db_client import Table
from src.main.lambdas.common.dynamo_schema import Bike
from src.main.lambdas.common.auth import get_caller_sub
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.api_gateway_response import api_response

ddb = DynamoDbClient()
table = ddb.dynamodb.Table(Table.BIKES)


def _is_owner(item: dict, caller_sub: str) -> bool:
    return item.get("owner_id") == caller_sub


def handler(event, context):
    method = event["httpMethod"]

    if method == "GET":
        response = table.get_item(Key={
            'id': event["queryStringParameters"]["id"]
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
        logger.info("deleted bike id {}".format(bike_id))
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
