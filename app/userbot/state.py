# For managing temporary state (multi-step commands) via Redis

import logging
from typing import Optional
from app.shared.redis_client import get_redis_async

logger = logging.getLogger("telegram_insight_agent.userbot.state")

async def store_status_message(request_id: str, message_id: int) -> None:
    """
    Store the Telegram message_id associated with a request_id in Redis.
    """
    logger.debug(f"Storing status message: request_id={request_id}, message_id={message_id}")
    redis = get_redis_async()
    try:
        await redis.set(f"status_msg:{request_id}", message_id)
        logger.info(f"Stored status message for request_id={request_id}")
    except Exception as e:
        logger.error(f"Error storing status message: {e}")
        raise
    finally:
        await redis.close()

async def get_status_message(request_id: str) -> Optional[int]:
    """
    Retrieve the Telegram message_id for the given request_id from Redis.
    """
    logger.debug(f"Getting status message for request_id={request_id}")
    redis = get_redis_async()
    try:
        val = await redis.get(f"status_msg:{request_id}")
        if val is not None:
            try:
                msg_id = int(val)
                logger.info(f"Retrieved status message: request_id={request_id}, message_id={msg_id}")
                return msg_id
            except Exception as e:
                logger.warning(f"Failed to convert status message id to int: {val} ({e})")
                return None
        logger.info(f"No status message found for request_id={request_id}")
        return None
    except Exception as e:
        logger.error(f"Error getting status message: {e}")
        return None
    finally:
        await redis.close()

# --- Pytest skeleton ---

"""
import pytest
from app.userbot.state import store_status_message, get_status_message

@pytest.mark.asyncio
async def test_store_status_message(monkeypatch):
    # monkeypatch get_redis_async().set to track calls
    pass

@pytest.mark.asyncio
async def test_get_status_message(monkeypatch):
    # monkeypatch get_redis_async().get to return a value
    pass
"""