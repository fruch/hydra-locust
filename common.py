import logging
import sys
import time
from functools import wraps
import random

import numpy as np
import boto3
import botocore
from locust import Locust, events
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy


class CqlLocust(Locust):  # pylint: disable=too-few-public-methods
    """
    This is the abstract Locust class which should be subclassed. It provides an CQL client
    that can be used to make CQL requests that will be tracked in Locust's statistics.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Cluster([self.host], protocol_version=4,
                              load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'))


class DynamodbLocust(Locust):  # pylint: disable=too-few-public-methods
    """
    This is the abstract Locust class which should be subclassed. It provides an dynamodb client
    that can be used to make dynamodb requests that will be tracked in Locust's statistics.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = botocore.config.Config(signature_version=botocore.UNSIGNED,
                                             max_pool_connections=50, inject_host_prefix=False, parameter_validation=False)

    def dynamodb_client(self):
        return boto3.resource('dynamodb', endpoint_url=self.host, use_ssl=False, verify=False, config=self.config)


def report_timings_cql(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)  # pylint: disable=unused-variable
        except Exception as exp:  # pylint: disable=broad-except
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="cql", name=func.__name__,
                                        response_time=total_time, response_length=0, exception=exp)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="cql", name=func.__name__,
                                        response_time=total_time, response_length=0)
    return wrapper


# TODO: remove this duplicate
def report_timings_dynamodb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)  # pylint: disable=unused-variable
        except Exception as exp:  # pylint: disable=broad-except
            logging.exception("failure")
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="dynamodb", name=func.__name__,
                                        response_time=total_time, response_length=0, exception=exp, tb=sys.exc_info()[2])
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="dynamodb", name=func.__name__,
                                        response_time=total_time, response_length=0)
    return wrapper


def iter_shuffle(iterable, bufsize=1000):
    """
    Shuffle an iterator. This works by holding `bufsize` items back
    and yielding them sometime later. This is NOT 100% random, proved or anything.
    idea from https://gist.github.com/andres-erbsen/1307752
    """
    iterable = iter(iterable)
    buf = []
    try:
        while True:
            for _ in range(random.randint(1, bufsize-len(buf))):
                buf.append(next(iterable))
            random.shuffle(buf)
            for _ in range(random.randint(1, bufsize)):
                if buf:
                    yield buf.pop()
                else:
                    break
    except StopIteration:
        random.shuffle(buf)
        while buf:
            yield buf.pop()
            return


def iter_zipf(n, alpha, num_samples):
    # idea from https://stackoverflow.com/q/31027739/459189

    # Calculate Zeta values from 1 to n:
    tmp = np.power(np.arange(1, n+1), -alpha)
    zeta = np.r_[0.0, np.cumsum(tmp)]
    # Store the translation map:
    dist_map = [x / zeta[-1] for x in zeta]

    while True:
        # Generate an array of uniform 0-1 pseudo-random values:
        u = np.random.random_sample(num_samples)
        # bisect them with dist_map
        v = np.searchsorted(dist_map, u)
        for t in v:
            yield t


if __name__ == "__main__":
    for i in iter_zipf(10000000, 2.0, 10000):
        print(i, end=" ")
