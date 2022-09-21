from itertools import cycle

# pylint: disable=wrong-import-position
from gevent import monkey

monkey.patch_all()

import numpy as np
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster  # pylint: disable=no-name-in-module
from cassandra.io.geventreactor import GeventConnection
from cassandra.policies import WhiteListRoundRobinPolicy
from locust import User, between, events, task

import prom_collector  # pylint: disable=unused-import
from common import iter_shuffle, iter_zipf, report_timings_cql

KEYS = cycle(iter_shuffle(range(1, 10000)))
READ = iter_zipf(10000, 2.0, num_samples=100)


@events.test_start.add_listener
def on_test_start(environment):
    addresses = [a.strip() for a in environment.host.split(",")]
    environment.client = Cluster(
        addresses,
        protocol_version=4,
        load_balancing_policy=WhiteListRoundRobinPolicy(addresses),
        connection_class=GeventConnection,
    )

    environment.session = environment.client.connect()
    environment.session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS keyspace1
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;
    """
    )
    environment.session.execute(
        """
        CREATE TABLE IF NOT EXISTS keyspace1.standard1 (
            key blob PRIMARY KEY,
            "C0" blob
        ) WITH compaction = {'class': 'SizeTieredCompactionStrategy'}
    """
    )
    environment.session.execute("USE keyspace1")

    environment.insert_stmt = environment.session.prepare(
        'INSERT INTO keyspace1.standard1 (key, "C0") VALUES (?, ?)'
    )
    environment.insert_stmt.consistency_level = ConsistencyLevel.LOCAL_ONE
    environment.read_stmt = environment.session.prepare(
        "SELECT * FROM keyspace1.standard1 WHERE key=?"
    )
    environment.read_stmt.consistency_level = ConsistencyLevel.LOCAL_ONE


class ApiUser(User):  # pylint: disable=too-few-public-methods
    def __init__(self, environment, **kwargs):
        super().__init__(environment, **kwargs)
        self.session = environment.session
        self.insert_stmt = environment.insert_stmt
        self.read_stmt = environment.read_stmt

    @report_timings_cql
    @task(10)
    def insert(self):
        key = next(KEYS)
        np.random.seed(key)
        self.session.execute(
            self.insert_stmt, (key.to_bytes(10, byteorder="big"), np.random.bytes(64))
        )

    @report_timings_cql
    @task(5)
    def read(self):
        key = next(READ)
        np.random.seed(key)
        data = np.random.bytes(64)
        res = self.session.execute(
            self.read_stmt, (int(key).to_bytes(10, byteorder="big"),)
        )
        assert res.one().C0 == data, f"key={int(key)} data validation failed"

    wait_time = between(0.00001, 0.00005)
