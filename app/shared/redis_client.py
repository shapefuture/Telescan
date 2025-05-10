# Redis connection & RQ Queue setup

import logging
from typing import Any
import redis.asyncio as aioredis
from rq import Queue
from config import settings

logger = logging.getLogger("telegram_insight_agent.redis_client")

def get_redis_sync() -> Any:
    """
    Get a synchronous Redis client (for RQ).
    """
    import redis
    logger.debug(f"Connecting to Redis (sync) at {settings.REDIS_URL}")
    try:
        client = redis.Redis.from_url(settings.REDIS_URL)
        logger.info("Connected to Redis (sync)")
        return client
    except Exception as e:
        logger.error(f"Error connecting to Redis (sync): {e}")
        raise

def get_redis_async() -> aioredis.Redis:
    """
    Get an async Redis client (for pub/sub, async ops).
    """
    logger.debug(f"Connecting to Redis (async) at {settings.REDIS_URL}")
    try:
        client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        logger.info("Connected to Redis (async)")
        return client
    except Exception as e:
        logger.error(f"Error connecting to Redis (async): {e}")
        raise

def get_rq_queue(name: str = "default") -> Queue:
    """
    Get an RQ queue for background jobs.
    """
    logger.debug(f"Getting RQ queue: {name}")
    try:
        queue = Queue(name, connection=get_redis_sync())
        logger.info(f"Created RQ queue: {name}")
        return queue
    except Exception as e:
        logger.error(f"Error creating RQ queue: {e}")
        raise

# --- Pytest skeleton for redis_client ---

"""
import pytest
from app.shared.redis_client import get_redis_sync, get_redis_async, get_rq_queue

def test_get_redis_sync(monkeypatch):
    # monkeypatch redis.Redis.from_url to return a mock
    pass

@pytest.mark.asyncio
async def test_get_redis_async(monkeypatch):
    # monkeypatch aioredis.from_url to return a mock
    pass

def test_get_rq_queue(monkeypatch):
    # monkeypatch get_redis_sync and Queue to return a mock queue
    pass
"""