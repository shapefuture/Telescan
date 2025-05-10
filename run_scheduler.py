"""
Entrypoint for RQ scheduler service for Telegram Insight Agent.
"""

import asyncio
import logging
from typing import NoReturn
from app.shared.database import async_sessionmaker
from app.worker.tasks import periodic_monitoring_check

logger = logging.getLogger("telegram_insight_agent.run_scheduler")

def main() -> NoReturn:
    """
    Start the RQ scheduler loop for periodic background task enqueuing.
    """
    logger.info("RQ Scheduler started. Will periodically trigger periodic_monitoring_check for all users with monitored chats.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scheduler_loop())

async def scheduler_loop() -> None:
    """
    Enqueue periodic monitoring jobs for each user with monitored chats.
    """
    while True:
        try:
            async with async_sessionmaker() as session:
                # Get all distinct user_ids with active monitored chats
                users = await session.execute(
                    "SELECT DISTINCT user_id FROM monitored_chats WHERE is_active = true"
                )
                user_ids = [row[0] for row in users.fetchall()]
                logger.info(f"Scheduler: Found {len(user_ids)} monitored users.")
                for user_id in user_ids:
                    try:
                        periodic_monitoring_check(user_id)
                        logger.debug(f"Scheduled periodic check for user_id={user_id}")
                    except Exception as e:
                        logger.error(f"Error scheduling for user {user_id}: {e}")
            await asyncio.sleep(3600)  # Run every hour
        except Exception as e:
            logger.error(f"Scheduler main loop error: {e}")
            await asyncio.sleep(60)  # Backoff and retry

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

# --- Pytest skeleton ---

"""
import pytest
import run_scheduler

def test_main_importable():
    assert hasattr(run_scheduler, "main")
"""