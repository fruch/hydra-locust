from itertools import cycle

import numpy as np
from locust import TaskSet, between, task

import prom_collector  # pylint: disable=unused-import
from common import CqlLocust, report_timings_cql, iter_zipf, iter_shuffle
from cassandra import ConsistencyLevel

KEYS = cycle(iter_shuffle(range(1, 10000)))
READ = iter_zipf(10000, 2.0, num_samples=100)


class CqlTaskSet(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None
        self.insert_stmt = None
        self.read_stmt = None

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

        self.insert_stmt = self.session.prepare("INSERT INTO standard1 (key, C0) VALUES (?, ?)")
        self.insert_stmt.consistency_level = ConsistencyLevel.QUORUM
        self.read_stmt = self.session.prepare("SELECT * FROM standard1 WHERE key=?")
        self.read_stmt.consistency_level = ConsistencyLevel.QUORUM

    @report_timings_cql
    @task(10)
    def insert(self):
        key = next(KEYS)
        np.random.seed(key)
        self.session.execute(self.insert_stmt, (key.to_bytes(10, byteorder='big'), np.random.bytes(64)))

    @report_timings_cql
    @task(5)
    def read(self):
        key = next(READ)
        np.random.seed(key)
        data = np.random.bytes(64)
        res = self.session.execute(self.read_stmt, (int(key).to_bytes(10, byteorder='big'), ))
        assert res.one().c0 == data, f"key={int(key)} data validation failed"


class ApiUser(CqlLocust):  # pylint: disable=too-few-public-methods

    wait_time = between(0.00001, 0.00005)
    task_set = CqlTaskSet
