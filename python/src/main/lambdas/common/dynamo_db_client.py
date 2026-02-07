from enum import StrEnum

import boto3

from src.main.lambdas.common.config import Config

DYNAMO_LOCAL_PORT = 9002


class Table(StrEnum):
    BIKES = "BIKES"
    USERS = "USERS"


class DynamoDbClient:
    def __init__(self):
        if Config.ENV == "LOCAL":
            self.dynamodb = boto3.resource(
                "dynamodb",
                region_name="us-east-1",
                endpoint_url="http://localhost:{}".format(DYNAMO_LOCAL_PORT),
                aws_access_key_id="dummy",
                aws_secret_access_key="dummy")

        else:
            self.dynamodb = boto3.resource("dynamodb")

    def preview_tables(self):
        """show up to 3 items from all tables"""
        table_names = Table.__members__.values()
        previews = {}
        for table_name in table_names:
            table = self.dynamodb.Table(table_name)
            response = table.scan(Limit=3)
            previews[table_name] = response.get("Items", [])
        return previews

    def get_item_from_table(self, key: str, table_name: Table):
        response = self.dynamodb.get_item(
            TableName=table_name,
            Key=key
        )
        if 'Item' in response:
            return response['Item']
        return {}
