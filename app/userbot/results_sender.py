# Responsible for sending result messages/files back to the user via Telethon

import os
import logging
from typing import Any, Optional

logger = logging.getLogger("telegram_insight_agent.userbot.results_sender")

async def send_llm_insight_and_files(
    client: Any,
    user_id: int,
    chat_title: str,
    summary_path: str,
    participants_file_path: Optional[str]
) -> None:
    """
    Send LLM summary and participants file to user via Telethon.

    Args:
        client: Telethon client.
        user_id: Telegram user ID.
        chat_title: Title of the chat.
        summary_path: Path to summary text file.
        participants_file_path: Path to participants file, or None.

    Returns:
        None
    """
    try:
        logger.info(f"Sending LLM insight and files to user_id={user_id}, chat_title={chat_title}")
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = f.read()
        msg = f"💡 Summary for {chat_title}:\n\n{summary[:4096]}"
        await client.send_message(user_id, msg)
        logger.info("Summary message sent.")
        if participants_file_path and os.path.exists(participants_file_path):
            await client.send_file(user_id, participants_file_path, caption="Participants list")
            logger.info("Participants file sent.")
            os.remove(participants_file_path)
            logger.info("Participants file removed from disk.")
    except Exception as e:
        logger.error(f"Error sending insight/files: {e}")

async def send_failure_insight_message(
    client: Any,
    user_id: int,
    chat_title: str,
    error_message: str
) -> None:
    """
    Send a failure message to user via Telethon.

    Args:
        client: Telethon client.
        user_id: Telegram user ID.
        chat_title: Title of the chat.
        error_message: Error string.

    Returns:
        None
    """
    try:
        logger.info(f"Sending failure message to user_id={user_id}, chat_title={chat_title}")
        await client.send_message(user_id, f"❌ Failed to process {chat_title}: {error_message}")
        logger.info("Failure message sent.")
    except Exception as e:
        logger.error(f"Error sending failure insight message: {e}")

# --- Pytest skeleton ---

"""
import pytest
from unittest.mock import AsyncMock, patch
from app.userbot import results_sender

@pytest.mark.asyncio
async def test_send_llm_insight_and_files(monkeypatch, tmp_path):
    client = AsyncMock()
    summary_path = tmp_path / "summary.txt"
    summary_path.write_text("Summary text here")
    participants_path = tmp_path / "participants.txt"
    participants_path.write_text("user list")
    await results_sender.send_llm_insight_and_files(client, 123, "Test Chat", str(summary_path), str(participants_path))
    client.send_message.assert_called()
    client.send_file.assert_called()
    # file is deleted
    assert not participants_path.exists()

@pytest.mark.asyncio
async def test_send_failure_insight_message(monkeypatch):
    client = AsyncMock()
    await results_sender.send_failure_insight_message(client, 123, "Fail Chat", "error msg")
    client.send_message.assert_called()
"""