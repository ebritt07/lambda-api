from src.main.lambdas.common.dynamo_db_client import DynamoDbClient
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.api_gateway_response import api_response

dynamodb = DynamoDbClient()


def handler(event, context):
    previews = dynamodb.preview_tables()
    logger.info(f"table previews:{previews}")
    return api_response(previews)
