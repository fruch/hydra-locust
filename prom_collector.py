from html import escape
from itertools import chain

import gevent
from prometheus_client import start_http_server, Metric, REGISTRY
from locust import runners
from locust.stats import sort_stats
from locust.util.rounding import proper_round


class LocustCollector:  # pylint: disable=too-few-public-methods
    @staticmethod
    def collect():
        stats = []
        for stat in chain(sort_stats(runners.locust_runner.request_stats), [runners.locust_runner.stats.total]):
            stats.append({
                "method": stat.method,
                "name": stat.name,
                "safe_name": escape(stat.name, quote=False),
                "num_requests": stat.num_requests,
                "num_failures": stat.num_failures,
                "avg_response_time": stat.avg_response_time,
                "min_response_time": 0 if stat.min_response_time is None else proper_round(stat.min_response_time),
                "max_response_time": proper_round(stat.max_response_time),
                "current_rps": stat.current_rps,
                "current_fail_per_sec": stat.current_fail_per_sec,
                "median_response_time": stat.median_response_time,
                "ninetieth_response_time": stat.get_response_time_percentile(0.9),
                "avg_content_length": stat.avg_content_length,
            })

        stats_metrics = ['avg_content_length', 'avg_response_time', 'current_rps', 'max_response_time',
                         'median_response_time', 'min_response_time', 'num_failures', 'num_requests']

        for mtr in stats_metrics:
            mtype = 'gauge'
            if mtr in ['num_requests', 'num_failures']:
                mtype = 'counter'
            metric = Metric('locust_requests_'+mtr, 'Locust requests '+mtr, mtype)
            for stat in stats:
                if not 'Aggregated' in stat['name']:
                    metric.add_sample(
                        'locust_requests_'+mtr, value=stat[mtr], labels={'path': stat['name'], 'method': stat.get('method', 'TOTAL')})
            yield metric


def loop():
    start_http_server(9000)
    REGISTRY.register(LocustCollector())


gevent.Greenlet.spawn_later(1, loop)
