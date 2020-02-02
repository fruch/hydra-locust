import time
from functools import wraps

import boto3

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
        self.client = boto3.resource('dynamodb', endpoint_url=self.host)


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
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="dynamodb", name=func.__name__,
                                        response_time=total_time, response_length=0, exception=exp)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="dynamodb", name=func.__name__,
                                        response_time=total_time, response_length=0)
    return wrapper
