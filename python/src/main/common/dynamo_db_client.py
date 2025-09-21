import boto3

from src.main.common.config import Config


class DynamoDbClient:
    def __init__(self):
        if Config.ENV == "LOCAL":
            self.dynamodb = boto3.client("dynamodb",
                                         region_name=Config.REGION,
                                         endpoint_url=Config.DYNAMODB_URL,
                                         aws_access_key_id="dummy",
                                         aws_secret_access_key="dummy")
        else:
            self.dynamodb = boto3.client("dynamodb",
                                         region_name=Config.REGION)

    def list_tables(self):
        return self.dynamodb.list_tables()
