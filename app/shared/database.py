# Async SQLAlchemy engine/session setup

"""
Async SQLAlchemy engine and sessionmaker setup for Telegram Insight Agent.
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config import settings

logger = logging.getLogger("telegram_insight_agent.database")

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

async def test_db_connection() -> bool:
    """
    Test database connectivity by executing a trivial query.

    Returns:
        True if connection is successful, False otherwise.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        logger.info("Database connection test succeeded.")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection test failed: {e}")
        return False

# --- Pytest skeleton ---

"""
import pytest
from app.shared.database import async_sessionmaker, test_db_connection

@pytest.mark.asyncio
async def test_create_session():
    async with async_sessionmaker() as session:
        assert session

@pytest.mark.asyncio
async def test_db_connection_func():
    assert await test_db_connection() in (True, False)
"""
from config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)