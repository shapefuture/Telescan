"""
Error handling utilities for Telegram Insight Agent.
"""

import logging
import asyncio
from typing import Optional

logger = logging.getLogger("telegram_insight_agent.error_handling")

def setup_asyncio_exception_logging(loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
    """
    Attach a global exception handler to asyncio event loop for uncaught exceptions.

    Args:
        loop: Optional event loop; defaults to current event loop.

    Returns:
        None
    """
    loop = loop or asyncio.get_event_loop()

    def handle_exception(loop, context):
        msg = context.get("exception", context["message"])
        logger.error(f"Uncaught asyncio exception: {msg}")

    loop.set_exception_handler(handle_exception)
    logger.info("Asyncio exception handler attached.")

# --- Pytest skeleton ---

"""
def test_setup_asyncio_exception_logging(monkeypatch):
    import asyncio
    from app.shared.error_handling import setup_asyncio_exception_logging
    loop = asyncio.get_event_loop()
    setup_asyncio_exception_logging(loop)
    # Simulate an exception
    try:
        loop.call_exception_handler({"message": "test error"})
    except Exception:
        assert False, "Exception should be handled and not raised"
"""