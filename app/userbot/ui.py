# Utilities for building Telegram keyboard layouts and formatting messages

import logging
from typing import Any, List, Optional

logger = logging.getLogger("telegram_insight_agent.userbot.ui")

def format_monitored_chats_list(chats: List[Any]) -> str:
    """
    Format a list of monitored chats as a Telegram HTML message.

    Args:
        chats: List of chat objects/dicts with chat_title and chat_id.

    Returns:
        Formatted string for Telegram.
    """
    logger.debug(f"Formatting monitored chats list: {chats}")
    if not chats:
        logger.info("No monitored chats to format.")
        return "No monitored chats."
    formatted = "\n".join([f"• <b>{c.chat_title}</b> (<code>{c.chat_id}</code>)" for c in chats])
    logger.debug("Formatted chat list.")
    return formatted

def build_settings_keyboard() -> Optional[list]:
    """
    Build an inline keyboard for /settings (for future expansion).

    Returns:
        Inline keyboard markup as a list (or None if not available).
    """
    logger.debug("Building /settings inline keyboard.")
    try:
        # Example: two buttons for "Show" and "Set Prompt"
        from telethon.tl.custom import Button
        keyboard = [
            [Button.inline("Show Prompt", b"settings_show")],
            [Button.inline("Set Prompt", b"settings_set")],
        ]
        logger.info("Built /settings keyboard.")
        return keyboard
    except ImportError:
        logger.warning("Telethon Button not available, skipping keyboard build.")
        return None
    except Exception as e:
        logger.error(f"Error building settings keyboard: {e}")
        return None

# --- Pytest skeleton ---

"""
def test_build_settings_keyboard_success(monkeypatch):
    class FakeButton:
        @staticmethod
        def inline(text, data): return (text, data)
    monkeypatch.setitem(__import__('sys').modules, 'telethon.tl.custom', type('Mod', (), {'Button': FakeButton}))
    from app.userbot.ui import build_settings_keyboard
    kb = build_settings_keyboard()
    assert kb is not None and len(kb) == 2
"""

async def update_manual_run_status_message(client: Any, request_id: str, status: str) -> None:
    """
    Edit the Telegram status message associated with a request_id to show progress.

    Args:
        client: Telethon client.
        request_id: Request/job identifier.
        status: Status string to show.

    Returns:
        None
    """
    from app.userbot.state import get_status_message
    logger.info(f"Updating status message for request_id={request_id} to status={status}")
    msg_id = await get_status_message(request_id)
    if not msg_id:
        logger.warning(f"No status message found for request_id={request_id}")
        return
    try:
        await client.edit_message("me", msg_id, f"Status: {status}")
        logger.info(f"Status message updated for request_id={request_id}")
    except Exception as e:
        logger.error(f"Failed to update status message: {e}")

# --- Pytest skeleton ---

"""
import pytest
from app.userbot.ui import format_monitored_chats_list

def test_format_monitored_chats_list_empty():
    assert format_monitored_chats_list([]) == "No monitored chats."

def test_format_monitored_chats_list_some():
    chats = [
        type("Chat", (), {"chat_title": "A", "chat_id": 123}),
        type("Chat", (), {"chat_title": "B", "chat_id": 456}),
    ]
    out = format_monitored_chats_list(chats)
    assert "A" in out and "B" in out and "123" in out and "456" in out

# For update_manual_run_status_message, use Telethon client mock and patch get_status_message
"""