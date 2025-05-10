"""
Telethon client and event handler registration for Telegram Insight Agent userbot.
"""

import logging
from typing import Any
from telethon import TelegramClient, events
from config import settings
from app.userbot import handlers

logger = logging.getLogger("telegram_insight_agent.userbot.client")

client = TelegramClient(
    settings.TELEGRAM_SESSION_PATH,
    settings.TELEGRAM_API_ID,
    settings.TELEGRAM_API_HASH
)

def register_handlers() -> None:
    """
    Register all userbot command handlers with the Telethon client.
    """
    logger.info("Registering userbot command handlers.")

    @client.on(events.NewMessage(pattern=r"^/monitor add"))
    async def _(event: Any):
        logger.debug("Handler: /monitor add")
        await handlers.handle_monitor_add(event)

    @client.on(events.NewMessage(pattern=r"^/monitor list$"))
    async def _(event: Any):
        logger.debug("Handler: /monitor list")
        await handlers.handle_monitor_list(event)

    @client.on(events.NewMessage(pattern=r"^/monitor remove"))
    async def _(event: Any):
        logger.debug("Handler: /monitor remove")
        await handlers.handle_monitor_remove(event)

    @client.on(events.NewMessage(pattern=r"^/monitor prompt"))
    async def _(event: Any):
        logger.debug("Handler: /monitor prompt")
        await handlers.handle_monitor_prompt(event)

    @client.on(events.NewMessage(pattern=r"^/monitor run"))
    async def _(event: Any):
        logger.debug("Handler: /monitor run")
        await handlers.handle_monitor_run(event)

    logger.info("All handlers registered.")

# --- Pytest skeleton ---

"""
import pytest
from app.userbot import client

def test_client_instance():
    assert hasattr(client, "client")
    assert callable(client.register_handlers)
"""

    @client.on(events.NewMessage(pattern=r"^/settings$"))
    async def _(event):
        await handlers.handle_settings(event)

    @client.on(events.NewMessage(pattern=r"^/settings set"))
    async def _(event):
        await handlers.handle_settings_set(event)

    @client.on(events.NewMessage(pattern=r"^/status$"))
    async def _(event):
        await handlers.handle_status(event)

    @client.on(events.NewMessage(pattern=r"^/pause"))
    async def _(event):
        await handlers.handle_pause(event)

    @client.on(events.NewMessage(pattern=r"^/resume"))
    async def _(event):
        await handlers.handle_resume(event)

    @client.on(events.NewMessage(pattern=r"^/cancel"))
    async def _(event):
        await handlers.handle_cancel(event)