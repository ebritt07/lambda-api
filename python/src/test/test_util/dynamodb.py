import os
import socket
import subprocess
import time

from src.main.lambdas.common.dynamo_db_client import DynamoDbClient, DYNAMO_LOCAL_PORT
from src.main.lambdas.common.logger import logger
from src.main.lambdas.common.dynamo_db_client import Table

TABLE_NAMES = Table.__members__.values()

STARTUP_TIMEOUT_SECONDS = 90


def wait_for_port(port, process, timeout=STARTUP_TIMEOUT_SECONDS):
    """Block until something accepts TCP connections on localhost:port.

    A cold `mvn exec:java` (e.g. on a fresh CI runner) can take well over a
    couple of seconds to start DynamoDB Local, so poll instead of sleeping.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                "DynamoDB Local exited early with code {}".format(process.returncode))
        try:
            with socket.create_connection(("localhost", int(port)), timeout=1):
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError(
        "DynamoDB Local not accepting connections on port {} after {}s".format(port, timeout))


def get_start_command():
    start_command = "mvn -f {}runDynamoLocally/pom.xml exec:java \
      -Dexec.mainClass=org.example.Main \
      -Dexec.args=\"{}\""
    path = ""
    if os.path.exists("runDynamoLocally"):
        return start_command.format(path, DYNAMO_LOCAL_PORT)
    if os.path.exists("src/test/runDynamoLocally"):
        return start_command.format("src/test/", DYNAMO_LOCAL_PORT)
    raise RuntimeError("cant find the dynamo path, cwd={}", os.getcwd())


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
        if os.environ["ENV"] != "LOCAL":
            raise RuntimeError("Env var must be LOCAL")

        os.environ.setdefault("AWS_ACCESS_KEY_ID", "test-id")
        os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test-key")

        logger.info(get_start_command())
        self.dynamodb_local_process = subprocess.Popen(get_start_command().split())
        self.running = True
        self.ddb_cli = DynamoDbClient()
        wait_for_port(DYNAMO_LOCAL_PORT, self.dynamodb_local_process)
        self.clean_all_tables()

        for table_name in TABLE_NAMES:
            create_kwargs = {
                "TableName": table_name,
                "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
                "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
                "BillingMode": "PAY_PER_REQUEST",
            }
            if table_name == Table.BIKES:
                create_kwargs["AttributeDefinitions"].append(
                    {"AttributeName": "owner_id", "AttributeType": "S"}
                )
                create_kwargs["GlobalSecondaryIndexes"] = [
                    {
                        "IndexName": "owner_id-index",
                        "KeySchema": [{"AttributeName": "owner_id", "KeyType": "HASH"}],
                        "Projection": {"ProjectionType": "ALL"},
                    }
                ]
            table = self.ddb_cli.dynamodb.create_table(**create_kwargs)
            table.wait_until_exists()
            logger.info("table '%s' created successfully", table_name)

    def terminate_local_dynamo(self):
        self.clean_all_tables()
        self.running = False
        if self.dynamodb_local_process is not None:
            self.dynamodb_local_process.terminate()
