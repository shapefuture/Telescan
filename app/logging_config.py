"""
Logging configuration for Telegram Insight Agent.
Sets up root logger, level, and format.
"""

import logging
from typing import Optional

def setup_logging(level: Optional[int] = None) -> None:
    """
    Configure root logger for the application.

    Args:
        level: Logging level (default: INFO, or from LOG_LEVEL env variable).

    Returns:
        None
    """
    log_level = level or getattr(logging, __import__("os").environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # Reduce SQLAlchemy noise
    logging.info(f"Logging configured at level: {logging.getLevelName(log_level)}")

# --- Pytest skeleton ---

"""
def test_setup_logging_runs():
    from app.logging_config import setup_logging
    setup_logging()
"""
