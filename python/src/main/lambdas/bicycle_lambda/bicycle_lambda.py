from dataclasses import asdict

from src.main.lambdas.common.dynamo_db_client import DynamoDbClient
from src.main.lambdas.common.dynamo_db_client import Table
from src.main.lambdas.common.dynamo_schema import Bike
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.api_gateway_response import api_response

ddb = DynamoDbClient()
table = ddb.dynamodb.Table(Table.BIKES)


def handler(event, context):
    logger.info(f"got an event: {event}")
    method = event["requestContext"]["http"]["method"]

    if method == "GET":
        response = table.get_item( Key={
            'id': event["queryStringParameters"]["id"]
            }
        )
        logger.info("result of get from table: {}", response)
        item = response.get('Item')
        if not item:
            return api_response({"message": "Bike not found"}, status_code=404)
        return api_response(item)

    if method == "PUT":
        bike_id = event["queryStringParameters"]["id"]
        response = table.get_item(Key={"id": bike_id})
        logger.info("result of get from table: {}", response)
        if not response.get("Item"):
            return api_response({"message": "Bike not found"}, status_code=404)

        bike_data = dict(event["body"])
        bike_data["id"] = bike_id
        bike = Bike(**bike_data)
        bike_dict = asdict(bike)
        result = table.put_item(Item=bike_dict)
        logger.info("result of put into table: {}", result)
        return api_response(bike)

    if method == "DELETE":
        bike_id = event["queryStringParameters"]["id"]
        response = table.get_item(Key={"id": bike_id})
        logger.info("result of get from table: {}", response)
        if not response.get("Item"):
            return api_response({"message": "Bike not found"}, status_code=404)

        result = table.delete_item(Key={"id": bike_id})
        logger.info("result of delete from table: {}", result)
        return api_response(None, status_code=204)


    bike = Bike(**event["body"])
    bike_dict = asdict(bike)
    result = table.put_item(
        Item=bike_dict
    )
    logger.info("result of put into table: {}", result)
    return api_response(bike)
