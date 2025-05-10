"""
Test helper utilities for Telegram Insight Agent.
"""

import logging
from typing import Any, Callable

logger = logging.getLogger("telegram_insight_agent.tests.helpers")

def assert_message_contains(message: str, substring: str) -> None:
    """
    Assert that a message contains a substring, with logging.

    Args:
        message: The full message string.
        substring: The expected substring.

    Raises:
        AssertionError if substring not found.
    """
    logger.debug(f"Asserting message contains substring: {substring!r}")
    if substring not in message:
        logger.error(f"Assertion failed: {substring!r} not in {message!r}")
        raise AssertionError(f"Expected '{substring}' in '{message}'")
    logger.info("Assertion passed.")

def mock_async_method(return_value: Any = None) -> Callable:
    """
    Create a mock async method that returns a given value.

    Args:
        return_value: Value to return.

    Returns:
        Async function.
    """
    async def _mock(*args, **kwargs):
        logger.debug(f"Mock async called, will return: {return_value!r}")
        return return_value
    return _mock

# --- Pytest skeleton ---

"""
def test_assert_message_contains_pass():
    from tests.helpers import assert_message_contains
    assert_message_contains("hello world", "world")

import pytest
def test_assert_message_contains_fail():
    from tests.helpers import assert_message_contains
    with pytest.raises(AssertionError):
        assert_message_contains("hello world", "notfound")

import asyncio
def test_mock_async_method():
    from tests.helpers import mock_async_method
    mock = mock_async_method(return_value=42)
    result = asyncio.run(mock())
    assert result == 42
"""