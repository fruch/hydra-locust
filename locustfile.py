# pylint: disable=wrong-import-position
from gevent import monkey  # noqa
monkey.patch_all()  # noqa

from itertools import cycle

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster  # pylint: disable=no-name-in-module
from cassandra.io.geventreactor import GeventConnection
from cassandra.policies import WhiteListRoundRobinPolicy
from locust import User, between, events, task
import numpy as np

# import prom_collector  # pylint: disable=unused-import
from common import iter_shuffle, iter_zipf, report_timings_cql

KEYS = cycle(iter_shuffle(range(1, 10000)))
READ = iter_zipf(10000, 2.0, num_samples=100)


class NewFancyUDT:

    def __init__(self, f1, f2):
        self.field_one = f1
        self.field_two = f2


@events.test_start.add_listener
def on_test_start(environment):
    keyspace = environment.parsed_options.keyspace
    table = environment.parsed_options.table
    addresses = [a.strip() for a in environment.host.split(",")]
    environment.client = Cluster(
        addresses,
        protocol_version=4,
        load_balancing_policy=WhiteListRoundRobinPolicy(addresses),
        connection_class=GeventConnection,
    )
    environment.session = environment.client.connect()
    environment.session.execute(
        f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}} AND durable_writes = true;
        """
    )
    environment.session.execute(f"USE {keyspace}")
    environment.session.execute("CREATE TYPE new_fancy_udt (f1 blob, f2 blob)")

    environment.session.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {keyspace}.{table} (
            key blob PRIMARY KEY,
            "C0" blob,
            "extra_udt" frozen <new_fancy_udt>
        ) WITH compaction = {{'class': 'SizeTieredCompactionStrategy'}}
        """
    )
    environment.client.register_user_type(keyspace, 'new_fancy_udt', NewFancyUDT)

    environment.insert_stmt = environment.session.prepare(
        f'INSERT INTO {keyspace}.{table} (key, "C0", "extra_udt") VALUES (?, ?, ?)'
    )
    environment.insert_stmt.consistency_level = ConsistencyLevel.LOCAL_ONE
    environment.read_stmt = environment.session.prepare(
        f"SELECT * FROM {keyspace}.{table} WHERE key=?"
    )
    environment.read_stmt.consistency_level = ConsistencyLevel.LOCAL_ONE


class ApiUser(User):  # pylint: disable=too-few-public-methods
    def __init__(self, environment, **_kwargs):
        super().__init__(environment)
        self.session = environment.session
        self.insert_stmt = environment.insert_stmt
        self.read_stmt = environment.read_stmt

    @report_timings_cql
    @task(10)
    def insert(self):
        key = next(KEYS)
        np.random.seed(key)
        self.session.execute(
            self.insert_stmt,
            (key.to_bytes(10, byteorder="big"), np.random.bytes(64), (np.random.bytes(16), np.random.bytes(16)))
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
