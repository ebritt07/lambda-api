from dataclasses import asdict
import json

from src.main.lambdas.common.dynamo_db_client import DynamoDbClient
from src.main.lambdas.common.dynamo_db_client import Table
from src.main.lambdas.common.dynamo_schema import Bike
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.api_gateway_response import api_response

ddb = DynamoDbClient()
table = ddb.dynamodb.Table(Table.BIKES)


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
        bike_id = event["queryStringParameters"]["id"]
        response = table.get_item(Key={"id": bike_id})
        if not response.get("Item"):
            return api_response({"message": "Bike not found"}, status_code=404)

        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)
        bike_data = dict(body)
        bike_data["id"] = bike_id
        bike = Bike(**bike_data)
        bike_dict = asdict(bike)
        table.put_item(Item=bike_dict)
        return api_response(bike)

    if method == "DELETE":
        bike_id = event["queryStringParameters"]["id"]
        response = table.get_item(Key={"id": bike_id})
        if not response.get("Item"):
            return api_response({"message": "Bike not found"}, status_code=404)

        table.delete_item(Key={"id": bike_id})
        logger.info("deleted bike id {}".format(bike_id))
        logger.info(bike_id)
        return api_response(None, status_code=204)

    body = event["body"]
    if isinstance(body, str):
        body = json.loads(body)
    bike = Bike(**body)
    bike_dict = asdict(bike)
    table.put_item(
        Item=bike_dict
    )
    return api_response(bike)
