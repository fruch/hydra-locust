import asyncio
import time

import aioboto3
import botocore
import numpy as np
from botocore.config import Config

KEYS = iter(range(1, 10000000))
COUNT = 0
START_TIME = time.time()


async def main():
    global COUNT  # pylint: disable=global-statement
    session = aioboto3.Session()
    config = Config(
        signature_version=botocore.UNSIGNED,
        max_pool_connections=50,
        inject_host_prefix=False,
        parameter_validation=False,
    )
    async with session.resource(
        "dynamodb",
        endpoint_url="http://127.0.0.1:8080",
        config=config,
        region_name="None",
    ) as dynamo_resource:  # pylint: disable=not-async-context-manager
        table = await dynamo_resource.Table("usertable")
        while True:
            requests = []
            start = time.time()
            for _ in range(10000):
                key = next(KEYS)
                np.random.seed(key)
                requests.append(
                    table.put_item(
                        Item={
                            "p": key.to_bytes(10, byteorder="big"),
                            "C0": np.random.bytes(64),
                        }
                    )
                )
            await asyncio.gather(*requests)
            COUNT += len(requests)
            elapsed = time.time() - start
            elapsed_since_start = time.time() - START_TIME
            print(COUNT, elapsed_since_start, elapsed, COUNT / elapsed_since_start)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(main())
