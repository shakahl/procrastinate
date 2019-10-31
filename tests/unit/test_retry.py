import pendulum
import pytest

from procrastinate import exceptions
from procrastinate import retry as retry_module


@pytest.mark.parametrize(
    "retry, expected_strategy",
    [
        (None, None),
        (12, retry_module.RetryStrategy(max_attempts=12)),
        (True, retry_module.RetryStrategy()),
        (
            retry_module.RetryStrategy(max_attempts=42),
            retry_module.RetryStrategy(max_attempts=42),
        ),
    ],
)
def test_get_retry_strategy(retry, expected_strategy):
    assert expected_strategy == retry_module.get_retry_strategy(retry)


@pytest.mark.parametrize(
    "attempts, wait, linear_wait, exponential_wait, schedule_in",
    [
        # No wait
        (0, 0.0, 0.0, 0.0, 0.0),
        # Constant, first try
        (1, 5.0, 0.0, 0.0, 5.0),
        # Constant, last try
        (9, 5.0, 0.0, 0.0, 5.0),
        # Constant, first non-retry
        (10, 5.0, 0.0, 0.0, None),
        # Constant, other non-retry
        (100, 5.0, 0.0, 0.0, None),
        # Linear (3 * 7)
        (3, 0.0, 7.0, 0.0, 21.0),
        # Exponential (2 ** (5+1))
        (5, 0.0, 0.0, 2.0, 64.0),
        # Mix & match 8 + 3*4 + 2**(4+1) = 52
        (4, 8.0, 3.0, 2.0, 52.0),
    ],
)
def test_get_schedule_in(attempts, schedule_in, wait, linear_wait, exponential_wait):
    strategy = retry_module.RetryStrategy(
        max_attempts=10,
        wait=wait,
        linear_wait=linear_wait,
        exponential_wait=exponential_wait,
    )
    assert strategy.get_schedule_in(attempts=attempts) == schedule_in


def test_get_retry_exception_returns_none():
    strategy = retry_module.RetryStrategy(max_attempts=10, wait=5.0)
    assert strategy.get_retry_exception(attempts=100) is None


def test_get_retry_exception_returns():
    strategy = retry_module.RetryStrategy(max_attempts=10, wait=5.0)

    now = pendulum.datetime(2000, 1, 1, tz="UTC")
    expected = pendulum.datetime(2000, 1, 1, 0, 0, 5, tz="UTC")
    with pendulum.test(now):
        exc = strategy.get_retry_exception(attempts=1)
        assert isinstance(exc, exceptions.JobRetry)
        assert exc.scheduled_at == expected