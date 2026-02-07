from src.main.lambdas.common.dynamo_db_client import DynamoDbClient
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.api_gateway_response import api_response

dynamodb = DynamoDbClient()

def handler(event, context):
    logger.info(f"got an event: {event}")
    tables = dynamodb.list_tables()
    logger.info(f"tables:{tables}")
    return api_response(tables)
