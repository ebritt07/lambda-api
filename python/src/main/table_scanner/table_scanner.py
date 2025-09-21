from src.main.common.dynamo_db_client import DynamoDbClient
from src.main.common.logger import logger

dynamodb = DynamoDbClient()

def handler(event, context):
    logger.info(f"got an event: {event}")
    tables = dynamodb.list_tables()
    logger.info(f"tables:{tables}")
    return tables
