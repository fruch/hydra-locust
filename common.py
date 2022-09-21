import logging
import random
import subprocess
import sys
import time
from functools import wraps

import configargparse
import numpy as np
from locust import events


@events.init_command_line_parser.add_listener
def add_checks_arguments(parser: configargparse.ArgumentParser):
    processes = parser.add_argument_group("start multiple worker processes")
    processes.add_argument(
        "--processes",
        "-p",
        action="store_true",
        help="start slave processes to start",
        env_var="LOCUST_PROCESSES",
        default=False,
    )


@events.init.add_listener
def on_locust_init(environment):
    if (
        environment.parsed_options.processes
        and environment.parsed_options.master
        and environment.parsed_options.expect_workers
    ):
        environment.worker_processes = []
        for _ in range(environment.parsed_options.expect_workers):
            args = [*sys.argv]
            args.remove("--master")
            args.remove("--processes")
            args.remove("--headless")
            i = args.index("--expect-workers")
            args.pop(i)
            args.pop(i)
            args = args[:5]
            p = subprocess.Popen(  # pylint: disable=consider-using-with
                args[:5] + ["--worker"], text=True, start_new_session=True
            )
            environment.worker_processes.append(p)


def report_timings_cql(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)  # pylint: disable=unused-variable
        except Exception as exp:  # pylint: disable=broad-except
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="cql",
                name=func.__name__,
                response_time=total_time,
                response_length=0,
                exception=exp,
            )
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="cql",
                name=func.__name__,
                response_time=total_time,
                response_length=0,
            )

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
            events.request_failure.fire(
                request_type="dynamodb",
                name=func.__name__,
                response_time=total_time,
                response_length=0,
                exception=exp,
                tb=sys.exc_info()[2],
            )
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="dynamodb",
                name=func.__name__,
                response_time=total_time,
                response_length=0,
            )

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
            for _ in range(random.randint(1, bufsize - len(buf))):
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
    tmp = np.power(np.arange(1, n + 1), -alpha)
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
    for num in iter_zipf(10000000, 2.0, 10000):
        print(num, end=" ")
