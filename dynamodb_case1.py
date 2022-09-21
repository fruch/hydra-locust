import logging
import uuid
from itertools import cycle

# pylint: disable=wrong-import-position
from gevent import monkey

monkey.patch_all()

import boto3
import botocore
import botocore.config
import numpy as np
from botocore.errorfactory import ClientError
from locust import User, between, events, run_single_user, task

import prom_collector  # pylint: disable=unused-import
from common import report_timings_dynamodb

KEYS = cycle(range(1, 1000000))
READ = cycle(iter(np.random.zipf(2, size=1000000)))


LOGGER = logging.getLogger(__name__)


@events.init.add_listener
def on_test_start(environment):
    table_name = "usertable"

    config = botocore.config.Config(
        signature_version=botocore.UNSIGNED,
        max_pool_connections=50,
        inject_host_prefix=False,
        parameter_validation=False,
    )
    dynamodb = environment.dynamo_resource = boto3.resource(
        "dynamodb",
        endpoint_url=environment.parsed_options.host,
        verify=False,
        region_name="None",
        config=config,
    )

    try:
        params = dict(
            TableName=table_name,
            BillingMode="PAY_PER_REQUEST",
            KeySchema=[{"AttributeName": "p", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "p", "AttributeType": "B"}],
        )

        table = dynamodb.create_table(**params)

        waiter = table.meta.client.get_waiter("table_exists")
        waiter.config.delay = 0.5
        waiter.config.max_attempts = 3
        waiter.wait(TableName=table_name)

    except ClientError as ex:
        # LOGGER.warning(str(ex))
        assert "already exists" in str(ex)

    environment.table = dynamodb.Table(table_name)


class DynamodbUser(User):  # pylint: disable=too-few-public-methods
    wait_time = between(0.00001, 0.00005)

    @report_timings_dynamodb
    @task(10)
    def insert(self):

        self.environment.table.put_item(
            Item={
                "p": next(KEYS).to_bytes(10, byteorder="big"),
                "C0": uuid.uuid1().bytes,
            }
        )

    @report_timings_dynamodb
    @task(5)
    def read(self):
        response = self.environment.table.get_item(
            Key={
                "p": int(next(READ)).to_bytes(10, byteorder="big"),
            }
        )
        item = response.get("Item", None)
        LOGGER.debug(item)


if __name__ == "__main__":
    run_single_user(DynamodbUser)
