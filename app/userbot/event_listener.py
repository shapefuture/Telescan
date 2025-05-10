# Listens to Redis Pub/Sub for job completion or progress events

import asyncio
import json
import logging
from typing import Any

from app.shared.redis_client import get_redis_async
from app.userbot.results_sender import send_llm_insight_and_files, send_failure_insight_message
from app.userbot.state import get_status_message
from app.userbot.ui import update_manual_run_status_message

logger = logging.getLogger("telegram_insight_agent.userbot.event_listener")

async def listen_for_job_events(client: Any, settings: Any) -> None:
    """
    Listen for job progress and completion events on Redis Pub/Sub and handle them.

    Args:
        client: Telethon client.
        settings: App config/settings.

    Returns:
        None
    """
    logger.info("Starting Redis pub/sub listener for job events.")
    redis = get_redis_async()
    pubsub = redis.pubsub()
    try:
        await pubsub.psubscribe("request_status:*")
        logger.info("Subscribed to Redis pubsub channel: request_status:*")
        async for msg in pubsub.listen():
            if msg["type"] == "pmessage":
                try:
                    data = json.loads(msg["data"])
                    status = data.get("status")
                    detail = data.get("detail")
                    key = msg["channel"]
                    request_id = key.split(":")[-1]
                    logger.debug(f"Received job event: request_id={request_id}, status={status}")
                    if status == "SUCCESS":
                        await handle_insight_job_completion(client, request_id, detail, failed=False)
                    elif status == "FAILED":
                        await handle_insight_job_completion(client, request_id, detail, failed=True)
                    elif status in ("TDL_HISTORY_EXPORT", "TDL_PARTICIPANTS_EXPORT", "CALLING_LLM"):
                        await update_manual_run_status_message(client, request_id, status)
                    elif status == "TDL_PARTICIPANTS_EXPORT_FAILED":
                        await update_manual_run_status_message(client, request_id, "Participants export failed")
                except Exception as e:
                    logger.error(f"Error processing pubsub event: {e} - msg: {msg}")
    except Exception as e:
        logger.error(f"Error in Redis pub/sub listen loop: {e}")
    finally:
        await pubsub.close()
        await redis.close()

async def handle_insight_job_completion(client: Any, request_id: str, detail: dict, failed: bool = False) -> None:
    """
    Handle the completion of an insight job, sending the results or failure message.

    Args:
        client: Telethon client.
        request_id: Job/request identifier.
        detail: Dict with job result paths and metadata.
        failed: Whether the job failed.

    Returns:
        None
    """
    logger.info(f"Handling insight job completion: request_id={request_id}, failed={failed}")
    msg_id = await get_status_message(request_id)
    user_id = detail.get("user_id")
    chat_title = detail.get("chat_title")
    try:
        if failed:
            await send_failure_insight_message(client, user_id, chat_title, str(detail))
            logger.info("Sent failure insight message.")
        else:
            await send_llm_insight_and_files(
                client,
                user_id,
                chat_title,
                detail.get("summary_path"),
                detail.get("participants_path"),
            )
            logger.info("Sent LLM insight and files.")
    except Exception as e:
        logger.error(f"Error handling job completion: {e}")

# --- Pytest skeleton ---

"""
import pytest
from unittest.mock import AsyncMock, patch
from app.userbot import event_listener

@pytest.mark.asyncio
async def test_handle_insight_job_completion_success(monkeypatch):
    client = AsyncMock()
    detail = {"user_id": 1, "chat_title": "Test", "summary_path": "/tmp/s.txt", "participants_path": "/tmp/p.txt"}
    monkeypatch.setattr(event_listener, "send_llm_insight_and_files", AsyncMock())
    await event_listener.handle_insight_job_completion(client, "request123", detail, failed=False)
    event_listener.send_llm_insight_and_files.assert_awaited()

@pytest.mark.asyncio
async def test_handle_insight_job_completion_failed(monkeypatch):
    client = AsyncMock()
    detail = {"user_id": 1, "chat_title": "Test"}
    monkeypatch.setattr(event_listener, "send_failure_insight_message", AsyncMock())
    await event_listener.handle_insight_job_completion(client, "request123", detail, failed=True)
    event_listener.send_failure_insight_message.assert_awaited()
"""