import os
import subprocess
import time
from typing import List

from src.main.lambdas.common.dynamo_db_client import DynamoDbClient, DYNAMO_LOCAL_PORT
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.dynamo_db_client import Table

TABLE_NAMES = [
   Table.BIKES,
   Table.USERS
]

START_COMMAND = "mvn -f runDynamoLocally/pom.xml exec:java \
  -Dexec.mainClass=org.example.Main \
  -Dexec.args=\"{}\"".format(DYNAMO_LOCAL_PORT)

class LocalDynamoManager():

    def __init__(self) -> None:
        self.ddb_cli = None
        self.dynamodb_local_process = None
        self.running = False

    def clean_all_tables(self):
        for table_name in TABLE_NAMES:
            table = self.ddb_cli.dynamodb.Table(table_name)
            try:
                table.delete()
                logger.info("Deleted {}".format(table_name))
            except Exception as e:
                continue

    def start_local_dynamo(self):
        logger.info(START_COMMAND)

        self.dynamodb_local_process = subprocess.Popen(START_COMMAND.split())
        self.running = True
        self.ddb_cli = DynamoDbClient()
        time.sleep(2)
        self.clean_all_tables()


        for table_name in TABLE_NAMES:
            table = self.ddb_cli.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            table.wait_until_exists()
            logger.info("table '%s' created successfully", table_name)

    def terminate_local_dynamo(self):
        self.clean_all_tables()
        self.running = False
        if self.dynamodb_local_process is not None:
            self.dynamodb_local_process.terminate()