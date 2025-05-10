"""
Script to initialize the database (create all tables) for Telegram Insight Agent.
"""

import asyncio
import logging
from app.shared.db_models import Base
from app.shared.database import engine

logger = logging.getLogger("telegram_insight_agent.init_db")

async def init_db() -> None:
    """
    Initialize the database by creating all tables defined in ORM models.
    """
    logger.info("Starting database initialization (create_all).")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created (create_all succeeded).")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())

# --- Pytest skeleton ---

"""
import pytest
from app.shared.init_db import init_db

@pytest.mark.asyncio
async def test_init_db_runs():
    # Should not raise
    await init_db()
"""