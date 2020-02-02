import uuid
from itertools import cycle

import numpy as np
from locust import TaskSet, between, task

import prom_collector  # pylint: disable=unused-import
from common import CqlLocust, report_timings

KEYS = cycle(range(1, 10000))
READ = cycle(iter(np.random.zipf(2, size=10000)))


class CqlTaskSet(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None

    def on_start(self):
        self.session = self.client.connect()
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS keyspace1
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'} AND durable_writes = true;
        """)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS keyspace1.standard1 (
                key blob PRIMARY KEY,
                C0 blob
            ) WITH compaction = {'class': 'SizeTieredCompactionStrategy'}
        """)
        self.session.execute("USE keyspace1")

    @report_timings
    @task(10)
    def insert(self):
        self.session.execute(
            """
            INSERT INTO standard1 (key, C0)
            VALUES (%s, %s)
            """,
            (next(KEYS).to_bytes(10, byteorder='big'), uuid.uuid1().bytes)
        )

    @report_timings
    @task(5)
    def read(self):
        self.session.execute(
            "SELECT * FROM standard1 WHERE key=%s", (int(next(READ)).to_bytes(10, byteorder='big'), )
        )


class ApiUser(CqlLocust):  # pylint: disable=too-few-public-methods

    wait_time = between(0.00001, 0.00005)
    task_set = CqlTaskSet
