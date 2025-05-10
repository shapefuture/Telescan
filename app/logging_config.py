"""
Logging configuration for Telegram Insight Agent.
Sets up root logger, level, and format.
"""

"""
Logging configuration for Telegram Insight Agent.
"""

import logging
from typing import Optional

def setup_logging(level: int = logging.INFO, log_format: Optional[str] = None) -> None:
    """
    Configure global logging format and level.

    Args:
        level: Logging level (default: logging.INFO).
        log_format: Optional format string.

    Returns:
        None
    """
    fmt = log_format or "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=level,
        format=fmt
    )
    logging.getLogger().info("Logging configured.")

# --- Pytest skeleton ---

"""
def test_setup_logging_runs():
    from app import logging_config
    logging_config.setup_logging()
""" -> None:
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
