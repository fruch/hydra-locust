"""Tests for common.py utilities: iter_shuffle, iter_zipf, and report_timings."""

import time
from itertools import islice
from unittest.mock import patch

from common import (
    iter_shuffle,
    iter_zipf,
    report_timings,
    report_timings_cql,
    report_timings_dynamodb,
)

# ---------------------------------------------------------------------------
# iter_shuffle tests
# ---------------------------------------------------------------------------


class TestIterShuffle:
    def test_produces_all_elements(self):
        """iter_shuffle must yield every element of the input exactly once."""
        data = list(range(100))
        result = list(iter_shuffle(data))
        assert sorted(result) == data

    def test_empty_input(self):
        """Shuffling an empty iterable should produce no elements."""
        assert list(iter_shuffle([])) == []

    def test_single_element(self):
        """A single-element input returns that element."""
        assert list(iter_shuffle([42])) == [42]

    def test_works_with_generator(self):
        """iter_shuffle should accept any iterable, not just lists."""
        gen = (x for x in range(50))
        result = list(iter_shuffle(gen, bufsize=10))
        assert sorted(result) == list(range(50))

    def test_custom_bufsize(self):
        """A small bufsize should still yield all elements."""
        data = list(range(200))
        result = list(iter_shuffle(data, bufsize=5))
        assert sorted(result) == data

    def test_output_is_reordered(self):
        """With high probability the output order differs from input order."""
        data = list(range(1000))
        result = list(iter_shuffle(data))
        # It's astronomically unlikely that a 1000-element shuffle is identical
        assert result != data


# ---------------------------------------------------------------------------
# iter_zipf tests
# ---------------------------------------------------------------------------


class TestIterZipf:
    def test_produces_values(self):
        """iter_zipf is an infinite generator; we can draw samples from it."""
        gen = iter_zipf(100, 2.0, num_samples=50)
        values = list(islice(gen, 200))
        assert len(values) == 200

    def test_values_in_range(self):
        """All values should be in [1, n]."""
        gen = iter_zipf(500, 2.0, num_samples=100)
        for val in islice(gen, 500):
            assert 1 <= val <= 500

    def test_skew_towards_small_values(self):
        """With alpha=2 the distribution is heavily skewed toward 1."""
        gen = iter_zipf(1000, 2.0, num_samples=1000)
        samples = list(islice(gen, 5000))
        low_count = sum(1 for v in samples if v <= 10)
        # At least 50% of values should be <= 10 for alpha=2.0
        assert low_count > len(samples) * 0.5


# ---------------------------------------------------------------------------
# report_timings tests
# ---------------------------------------------------------------------------


class TestReportTimings:
    def test_report_timings_fires_success_event(self):
        """On success, report_timings fires a Locust request event with no exception."""
        with patch("common.events") as mock_events:
            @report_timings("cql")
            def my_func():
                pass

            my_func()
            mock_events.request.fire.assert_called_once()
            call_kwargs = mock_events.request.fire.call_args[1]
            assert call_kwargs["request_type"] == "cql"
            assert call_kwargs["name"] == "my_func"
            assert call_kwargs["exception"] is None
            assert call_kwargs["response_length"] == 0

    def test_report_timings_fires_failure_event(self):
        """On exception, report_timings fires a Locust request event with the exception."""
        with patch("common.events") as mock_events:
            @report_timings("dynamodb")
            def failing_func():
                raise ValueError("boom")

            failing_func()  # should not propagate
            mock_events.request.fire.assert_called_once()
            call_kwargs = mock_events.request.fire.call_args[1]
            assert call_kwargs["request_type"] == "dynamodb"
            assert call_kwargs["name"] == "failing_func"
            assert isinstance(call_kwargs["exception"], ValueError)

    def test_report_timings_measures_time(self):
        """Reported response_time should approximate real elapsed time."""
        with patch("common.events") as mock_events:
            @report_timings("cql")
            def slow_func():
                time.sleep(0.05)

            slow_func()
            call_kwargs = mock_events.request.fire.call_args[1]
            assert call_kwargs["response_time"] >= 40  # at least ~40 ms

    def test_custom_request_type(self):
        """report_timings accepts arbitrary request type strings."""
        with patch("common.events") as mock_events:
            @report_timings("grpc")
            def grpc_call():
                pass

            grpc_call()
            call_kwargs = mock_events.request.fire.call_args[1]
            assert call_kwargs["request_type"] == "grpc"

    def test_backward_compat_cql_alias(self):
        """report_timings_cql is a ready-made decorator for request_type='cql'."""
        with patch("common.events") as mock_events:
            @report_timings_cql
            def cql_op():
                pass

            cql_op()
            call_kwargs = mock_events.request.fire.call_args[1]
            assert call_kwargs["request_type"] == "cql"

    def test_backward_compat_dynamodb_alias(self):
        """report_timings_dynamodb is a ready-made decorator for request_type='dynamodb'."""
        with patch("common.events") as mock_events:
            @report_timings_dynamodb
            def ddb_op():
                pass

            ddb_op()
            call_kwargs = mock_events.request.fire.call_args[1]
            assert call_kwargs["request_type"] == "dynamodb"

    def test_preserves_function_name(self):
        """The decorated function should preserve its original __name__."""
        @report_timings("test")
        def original_name():
            pass

        assert original_name.__name__ == "original_name"
