"""
Pytest configuration and test fixtures for Telegram Insight Agent.
"""

import logging
import pytest
from typing import AsyncGenerator
from app.shared.database import async_sessionmaker

logger = logging.getLogger("telegram_insight_agent.tests.conftest")

@pytest.fixture(scope="session")
def event_loop():
    """
    Use a single event loop for all async tests in the session.
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_test_session() -> AsyncGenerator:
    """
    Async SQLAlchemy DB session fixture for tests.
    Rolls back at teardown.
    """
    logger.info("Creating async test database session.")
    async with async_sessionmaker() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Test session error: {e}")
            raise
        finally:
            await session.rollback()
            logger.info("Rolled back test session.")

# Add more fixtures as needed for Telethon client, Redis, etc.