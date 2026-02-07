from enum import StrEnum

import boto3

from src.main.lambdas.common.config import Config

DYNAMO_LOCAL_PORT = 9001

class Table(StrEnum):
    BIKES = "BIKES"
    USERS = "USERS"

class DynamoDbClient:
    def __init__(self):
        if Config.ENV == "LOCAL":
            self.dynamodb = boto3.resource("dynamodb",
                                             region_name="us-east-1",
                                             endpoint_url="http://localhost:{}".format(DYNAMO_LOCAL_PORT),
                                             aws_access_key_id="dummy",
                                             aws_secret_access_key="dummy")

        else:
            self.dynamodb = boto3.resource("dynamodb")

    def list_tables(self):
        return self.dynamodb.list_tables()


    def get_item_from_table(self, key: str, table_name: Table):
        response = self.dynamodb.get_item(
            TableName=table_name,
            Key=key
        )
        if 'Item' in response:
            return response['Item']
        return {}
