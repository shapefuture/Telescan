"""
Generic utility functions for Telegram Insight Agent.
"""

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("telegram_insight_agent.shared.utils")

def safe_format_datetime(dt: Optional[datetime], fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Safely format a datetime object to string.

    Args:
        dt: datetime object or None.
        fmt: Format string (default "%Y-%m-%d %H:%M:%S").

    Returns:
        Formatted string, or "N/A" if dt is None or error occurs.
    """
    try:
        if dt is None:
            logger.warning("safe_format_datetime: dt is None")
            return "N/A"
        result = dt.strftime(fmt)
        logger.debug(f"Formatted datetime {dt} as {result}")
        return result
    except Exception as e:
        logger.error(f"Error formatting datetime: {e}")
        return "N/A"

def truncate_text(text: str, max_length: int = 80) -> str:
    """
    Truncate a string to a maximum length, adding ellipsis if needed.

    Args:
        text: The input string.
        max_length: Maximum allowed length.

    Returns:
        Truncated string.
    """
    try:
        if len(text) > max_length:
            truncated = text[:max_length-3] + "..."
            logger.debug(f"Truncated text from {len(text)} to {max_length}: {truncated!r}")
            return truncated
        logger.debug(f"Text within limit: {text!r}")
        return text
    except Exception as e:
        logger.error(f"Error in truncate_text: {e}")
        return text

# --- Pytest skeleton ---

"""
def test_safe_format_datetime_normal():
    from app.shared.utils import safe_format_datetime
    import datetime
    assert safe_format_datetime(datetime.datetime(2020, 1, 2, 3, 4, 5)) == "2020-01-02 03:04:05"

def test_safe_format_datetime_none():
    from app.shared.utils import safe_format_datetime
    assert safe_format_datetime(None) == "N/A"

def test_truncate_text_truncates():
    from app.shared.utils import truncate_text
    assert truncate_text("a" * 100, 10) == "aaaaaaa..."

def test_truncate_text_no_truncate():
    from app.shared.utils import truncate_text
    assert truncate_text("short", 10) == "short"
"""