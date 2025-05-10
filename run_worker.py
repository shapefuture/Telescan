"""
Entrypoint for RQ worker service for Telegram Insight Agent.
"""

import logging
from typing import NoReturn
from rq import Worker
from app.shared.redis_client import get_redis_sync
import app.worker.tasks  # noqa: F401, ensure tasks are registered

logger = logging.getLogger("telegram_insight_agent.run_worker")

def main() -> NoReturn:
    """
    Start the RQ worker for background job processing.
    """
    logger.info("Starting RQ Worker main routine.")
    try:
        redis_conn = get_redis_sync()
        worker = Worker(["default"], connection=redis_conn)
        logger.info("RQ Worker starting...")
        worker.work()
    except Exception as e:
        logger.error(f"RQ Worker crashed: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

# --- Pytest skeleton ---

"""
import pytest
from unittest.mock import patch

def test_main_importable():
    import run_worker
    assert hasattr(run_worker, "main")
"""