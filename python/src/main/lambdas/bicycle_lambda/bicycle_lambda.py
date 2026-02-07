from dataclasses import asdict

from src.main.lambdas.common.dynamo_db_client import DynamoDbClient
from src.main.lambdas.common.dynamo_db_client import Table
from src.main.lambdas.common.dynamo_schema import Bike
from src.main.lambdas.common.logger import logger

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
        return response.get('Item', {})


    bike = Bike(**event["body"])
    bike_dict = asdict(bike)
    result = table.put_item(
        Item=bike_dict
    )
    logger.info("result of put into table: {}", result)
    return bike


