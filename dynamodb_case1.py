import logging
import uuid
from itertools import cycle

import numpy as np
from botocore.errorfactory import ClientError
from locust import TaskSet, between, task

import prom_collector  # pylint: disable=unused-import
from common import DynamodbLocust, report_timings_dynamodb

KEYS = cycle(range(1, 1000000))
READ = cycle(iter(np.random.zipf(2, size=1000000)))


LOGGER = logging.getLogger(__name__)


class DynamodbTaskSet(TaskSet):
    table_name = 'usertable'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = None
        self.dynamodb = None

    def setup(self):
        dynamodb = self.locust.dynamodb_client()
        try:
            params = dict(TableName=self.table_name,
                          BillingMode='PAY_PER_REQUEST',
                          KeySchema=[{'AttributeName': 'p', 'KeyType': 'HASH'}],
                          AttributeDefinitions=[
                              {'AttributeName': 'p', 'AttributeType': 'B'}])

            table = dynamodb.create_table(**params)

            waiter = table.meta.client.get_waiter('table_exists')
            waiter.config.delay = 0.5
            waiter.config.max_attempts = 3
            waiter.wait(TableName=self.table_name)

        except ClientError as ex:
            # LOGGER.warning(str(ex))
            assert 'already exists' in str(ex)

    def on_start(self):
        self.dynamodb = self.locust.dynamodb_client()
        self.table = self.dynamodb.Table(self.table_name)

    @report_timings_dynamodb
    @task(10)
    def insert(self):

        self.table.put_item(
            Item={
                'p':  next(KEYS).to_bytes(10, byteorder='big'),
                'C0': uuid.uuid1().bytes
            }
        )

    @report_timings_dynamodb
    @task(5)
    def read(self):
        response = self.table.get_item(
            Key={
                'p':  int(next(READ)).to_bytes(10, byteorder='big'),
            }
        )
        item = response.get('Item', None)
        LOGGER.debug(item)


class ApiUser(DynamodbLocust):  # pylint: disable=too-few-public-methods
    wait_time = between(0.00001, 0.00005)
    task_set = DynamodbTaskSet
