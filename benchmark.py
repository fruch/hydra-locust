import time

import boto3
import botocore
import numpy as np
from botocore.config import Config

KEYS = iter(range(1, 10000))


def main():
    count = 0
    start_time = time.time()

    def set_connection_header(
        request, operation_name, **kwargs
    ):  # pylint: disable=unused-argument
        request.headers["Connection"] = "keep-alive"

    session = boto3.Session()
    session.events.register("request-created.dynamodb", set_connection_header)

    config = Config(
        signature_version=botocore.UNSIGNED,
        max_pool_connections=10,
        inject_host_prefix=False,
        parameter_validation=False,
    )
    dynamodb = session.resource(
        "dynamodb", endpoint_url="http://127.0.0.1:8080", config=config
    )

    table = dynamodb.Table("usertable")
    while True:
        start = time.time()
        key = next(KEYS)
        np.random.seed(key)
        table.put_item(
            Item={"p": key.to_bytes(10, byteorder="big"), "C0": np.random.bytes(64)}
        )
        count += 1
        elapsed = time.time() - start
        elapsed_since_start = time.time() - start_time
        if count % 100 == 0:
            print(count, elapsed_since_start, elapsed, count / elapsed_since_start)


main()
