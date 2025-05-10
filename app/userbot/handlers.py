# Userbot command/callback handlers

from app.shared.database import async_sessionmaker
from app.shared.db_crud import (
    add_monitored_chat, get_all_monitored_chats_for_user, remove_monitored_chat, update_monitored_chat_prompt,
    set_chat_active, get_latest_run_status, set_default_prompt, get_default_prompt
)
from app.userbot.ui import format_monitored_chats_list
from app.shared.db_crud import get_monitored_chat
from app.worker.tasks import process_monitored_chat
import asyncio

import logging
from typing import Any
from telethon.events.newmessage import NewMessage
from telethon.tl.custom import Message

logger = logging.getLogger("telegram_insight_agent.userbot.handlers")

async def handle_monitor_add(event: NewMessage.Event) -> None:
    """
    Handle /monitor add <chat_id> <prompt>
    """
    logger.info(f"handle_monitor_add: raw_text={getattr(event, 'raw_text', None)!r}")
    try:
        # Accept both numeric IDs and @usernames
        parts = event.raw_text.split(maxsplit=3)
        if len(parts) < 4:
            await event.reply("Usage: /monitor add <chat_id> <prompt>")
            logger.warning("Monitor add: not enough arguments")
            return
        _, _, chat_id_raw, prompt = parts
        # Try to resolve chat_id and title using Telethon
        entity = await event.client.get_entity(chat_id_raw)
        chat_id = entity.id
        chat_title = getattr(entity, "title", getattr(entity, "username", str(chat_id)))
        user_id = event.sender_id
        logger.info(f"Adding monitor for user_id={user_id}, chat_id={chat_id}, title={chat_title}")
        async with async_sessionmaker() as session:
            # Check if already monitored
            existing = await get_monitored_chat(session, user_id, chat_id)
            if existing:
                await event.reply(f"Already monitoring {chat_title} ({chat_id}).")
                logger.warning("Monitor add: already monitored")
                return
            mc = await add_monitored_chat(session, user_id, chat_id, chat_title, prompt)
            await event.reply(f"Added monitoring for {chat_title} ({chat_id}).")
            logger.info(f"Monitor add: success for user_id={user_id}, chat_id={chat_id}")
    except Exception as e:
        logger.exception(f"Failed to add monitoring: {e}")
        await event.reply(f"Failed to add monitoring: {e}")

# ... other handlers above ...

from app.shared.db_crud import get_recent_jobs_for_user

async def handle_status(event: Any) -> None:
    """
    Handle the /status command for showing recent job status.

    Usage:
        /status

    Shows recent job runs (manual/scheduled) for the user.
    """
    logger.info(f"handle_status called: raw_text={getattr(event, 'raw_text', None)!r}")
    try:
        user_id = event.sender_id
        async with async_sessionmaker() as session:
            jobs = await get_recent_jobs_for_user(session, user_id, limit=10)
        if not jobs:
            await event.reply("You have no recent monitored chat runs.")
            logger.info(f"No recent jobs for user_id={user_id}")
            return
        lines = []
        for job in jobs:
            lines.append(
                f"<b>{job.chat_title}</b> (<code>{job.chat_id}</code>): "
                f"<code>{job.status}</code> {job.detail or ''} "
                f"<i>{job.created_at.strftime('%Y-%m-%d %H:%M')}</i>"
            )
        msg = "Recent monitored chat runs:\n\n" + "\n".join(lines)
        await event.reply(msg)
        logger.info(f"Sent recent job status for user_id={user_id}")
    except Exception as e:
        logger.exception(f"Failed to process /status: {e}")
        await event.reply(f"Failed to process /status: {e}")

"""
# Pytest skeleton

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.userbot import handlers

@pytest.mark.asyncio
async def test_handle_status_no_jobs(monkeypatch):
    event = MagicMock()
    event.sender_id = 42
    event.reply = AsyncMock()
    monkeypatch.setattr(handlers, "get_recent_jobs_for_user", AsyncMock(return_value=[]))
    await handlers.handle_status(event)
    event.reply.assert_called_with("You have no recent monitored chat runs.")

@pytest.mark.asyncio
async def test_handle_status_some_jobs(monkeypatch):
    event = MagicMock()
    event.sender_id = 42
    event.reply = AsyncMock()
    Job = type("Job", (), {})
    job = Job()
    job.chat_title = "Test"
    job.chat_id = 123
    job.status = "SUCCESS"
    job.detail = "ok"
    import datetime
    job.created_at = datetime.datetime.now()
    monkeypatch.setattr(handlers, "get_recent_jobs_for_user", AsyncMock(return_value=[job]))
    await handlers.handle_status(event)
    event.reply.assert_called()
    assert "Test" in event.reply.call_args[0][0]
"""

import logging
from typing import Any
from app.shared.database import async_sessionmaker
from app.shared.db_crud import set_default_prompt, get_default_prompt

logger = logging.getLogger("telegram_insight_agent.userbot.handlers")

async def handle_settings(event: Any) -> None:
    """
    Handle the /settings command for getting/setting user default prompt.

    Usage:
        /settings               -- show current default prompt
        /settings set <prompt>  -- set new default prompt
    """
    logger.info(f"handle_settings called: raw_text={getattr(event, 'raw_text', None)!r}")
    try:
        parts = event.raw_text.strip().split(maxsplit=2)
        user_id = event.sender_id
        if len(parts) == 1 or (len(parts) == 2 and parts[1] == "show"):
            # Show current default prompt
            async with async_sessionmaker() as session:
                prompt = await get_default_prompt(session, user_id)
            msg = f"Your default LLM prompt is:\n\n<code>{prompt or 'Not set'}</code>"
            await event.reply(msg)
            logger.info(f"Replied with current prompt for user_id={user_id}")
        elif len(parts) >= 3 and parts[1] == "set":
            new_prompt = parts[2]
            async with async_sessionmaker() as session:
                await set_default_prompt(session, user_id, new_prompt)
            await event.reply(f"Default prompt updated to:\n\n<code>{new_prompt}</code>")
            logger.info(f"Default prompt updated for user_id={user_id}")
        else:
            msg = ("/settings — show your default prompt\n"
                   "/settings set <prompt> — set your default prompt")
            await event.reply(msg)
            logger.warning("Settings: invalid usage")
    except Exception as e:
        logger.exception(f"Failed to process /settings: {e}")
        await event.reply(f"Failed to process /settings: {e}")

# Register this handler in client.py as:
# @client.on(events.NewMessage(pattern=r"^/settings"))
# async def _(event): await handlers.handle_settings(event)

"""
# Pytest skeleton

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.userbot import handlers

@pytest.mark.asyncio
async def test_handle_settings_show(monkeypatch):
    event = MagicMock()
    event.raw_text = "/settings"
    event.sender_id = 42
    event.reply = AsyncMock()
    monkeypatch.setattr(handlers, "get_default_prompt", AsyncMock(return_value="abc"))
    monkeypatch.setattr(handlers, "set_default_prompt", AsyncMock())
    await handlers.handle_settings(event)
    event.reply.assert_called()
    assert "abc" in event.reply.call_args[0][0]

@pytest.mark.asyncio
async def test_handle_settings_set(monkeypatch):
    event = MagicMock()
    event.raw_text = "/settings set new"
    event.sender_id = 42
    event.reply = AsyncMock()
    monkeypatch.setattr(handlers, "set_default_prompt", AsyncMock())
    await handlers.handle_settings(event)
    event.reply.assert_called_with("Default prompt updated to:\n\n<code>new</code>")

@pytest.mark.asyncio
async def test_handle_settings_invalid(monkeypatch):
    event = MagicMock()
    event.raw_text = "/settings foo"
    event.sender_id = 42
    event.reply = AsyncMock()
    await handlers.handle_settings(event)
    event.reply.assert_called()
"""

# --- Pytest skeleton for handlers ---

"""
import pytest
from unittest.mock import AsyncMock, MagicMock
import app.userbot.handlers as handlers

@pytest.mark.asyncio
async def test_handle_monitor_add_already_monitored(monkeypatch):
    event = MagicMock()
    event.raw_text = "/monitor add 123 test"
    event.client.get_entity = AsyncMock(return_value=MagicMock(id=123, title="Test Chat"))
    event.sender_id = 42
    event.reply = AsyncMock()
    # Patch get_monitored_chat to return a dummy value
    monkeypatch.setattr(handlers, "get_monitored_chat", AsyncMock(return_value=object()))
    await handlers.handle_monitor_add(event)
    event.reply.assert_called_with("Already monitoring Test Chat (123).")

@pytest.mark.asyncio
async def test_handle_monitor_add_success(monkeypatch):
    event = MagicMock()
    event.raw_text = "/monitor add 123 test"
    event.client.get_entity = AsyncMock(return_value=MagicMock(id=123, title="Test Chat"))
    event.sender_id = 42
    event.reply = AsyncMock()
    monkeypatch.setattr(handlers, "get_monitored_chat", AsyncMock(return_value=None))
    monkeypatch.setattr(handlers, "add_monitored_chat", AsyncMock())
    await handlers.handle_monitor_add(event)
    event.reply.assert_called_with("Added monitoring for Test Chat (123).")
"""

async def handle_monitor_list(event):
    user_id = event.sender_id
    async with async_sessionmaker() as session:
        chats = await get_all_monitored_chats_for_user(session, user_id)
        msg = format_monitored_chats_list(chats)
        await event.reply(msg)

async def handle_settings(event):
    user_id = event.sender_id
    async with async_sessionmaker() as session:
        current = await get_default_prompt(session, user_id)
    buttons = [
        [{"text": "Set Default Prompt", "callback_data": "set_prompt"}]
    ]
    msg = f"Your current default prompt: <b>{current or 'Not set'}</b>\n\nSend /settings set &lt;your prompt&gt; to update."
    await event.reply(msg, buttons=buttons)

async def handle_settings_set(event):
    user_id = event.sender_id
    parts = event.raw_text.split(maxsplit=2)
    if len(parts) < 3:
        await event.reply("Usage: /settings set <prompt>")
        return
    prompt = parts[2]
    async with async_sessionmaker() as session:
        await set_default_prompt(session, user_id, prompt)
    await event.reply("Default prompt updated.")

async def handle_status(event):
    user_id = event.sender_id
    async with async_sessionmaker() as session:
        statuses = await get_latest_run_status(session, user_id)
    if not statuses:
        await event.reply("No monitored chats found.")
        return
    msg = "Latest run status (per chat):\n"
    for chat_id, title, last_id in statuses:
        msg += f"• <b>{title}</b> (<code>{chat_id}</code>): Last processed message ID: <code>{last_id}</code>\n"
    await event.reply(msg)

async def handle_pause(event):
    user_id = event.sender_id
    parts = event.raw_text.split()
    if len(parts) < 3:
        await event.reply("Usage: /pause <chat_id>")
        return
    chat_id_raw = parts[2]
    entity = await event.client.get_entity(chat_id_raw)
    chat_id = entity.id
    async with async_sessionmaker() as session:
        rc = await set_chat_active(session, user_id, chat_id, False)
    if rc:
        await event.reply(f"Paused monitoring for chat {chat_id}.")
    else:
        await event.reply(f"Could not pause monitoring (not found or already paused).")

async def handle_resume(event):
    user_id = event.sender_id
    parts = event.raw_text.split()
    if len(parts) < 3:
        await event.reply("Usage: /resume <chat_id>")
        return
    chat_id_raw = parts[2]
    entity = await event.client.get_entity(chat_id_raw)
    chat_id = entity.id
    async with async_sessionmaker() as session:
        rc = await set_chat_active(session, user_id, chat_id, True)
    if rc:
        await event.reply(f"Resumed monitoring for chat {chat_id}.")
    else:
        await event.reply(f"Could not resume monitoring (not found or already active).")

async def handle_cancel(event):
    parts = event.raw_text.split()
    if len(parts) < 2:
        await event.reply("Usage: /cancel <request_id>")
        return
    request_id = parts[1]
    from rq import Queue
    from app.shared.redis_client import get_redis_sync
    rq = Queue(connection=get_redis_sync())
    job = rq.fetch_job(request_id)
    if job:
        job.cancel()
        await event.reply(f"Cancelled job {request_id}")
        # Optionally update status message in Telegram
        from app.userbot.ui import update_manual_run_status_message
        await update_manual_run_status_message(event.client, request_id, "CANCELLED")
    else:
        await event.reply("Job not found or already finished.")

async def handle_monitor_remove(event):
    """Usage: /monitor remove <chat_id>"""
    try:
        parts = event.raw_text.split()
        if len(parts) < 3:
            await event.reply("Usage: /monitor remove <chat_id>")
            return
        _, _, chat_id_raw = parts
        entity = await event.client.get_entity(chat_id_raw)
        chat_id = entity.id
        user_id = event.sender_id
        async with async_sessionmaker() as session:
            rc = await remove_monitored_chat(session, user_id, chat_id)
            if rc:
                await event.reply(f"Removed monitoring for chat {chat_id}.")
            else:
                await event.reply(f"No such monitored chat found for removal.")
    except Exception as e:
        await event.reply(f"Failed to remove monitoring: {e}")

async def handle_monitor_prompt(event):
    """Usage: /monitor prompt <chat_id> <new_prompt>"""
    try:
        parts = event.raw_text.split(maxsplit=3)
        if len(parts) < 4:
            await event.reply("Usage: /monitor prompt <chat_id> <new_prompt>")
            return
        _, _, chat_id_raw, new_prompt = parts
        entity = await event.client.get_entity(chat_id_raw)
        chat_id = entity.id
        user_id = event.sender_id
        async with async_sessionmaker() as session:
            rc = await update_monitored_chat_prompt(session, user_id, chat_id, new_prompt)
            if rc:
                await event.reply(f"Updated prompt for chat {chat_id}.")
            else:
                await event.reply(f"No such monitored chat to update.")
    except Exception as e:
        await event.reply(f"Failed to update prompt: {e}")

async def handle_monitor_run(event):
    """Usage: /monitor run <chat_id>"""
    try:
        parts = event.raw_text.split()
        if len(parts) < 3:
            await event.reply("Usage: /monitor run <chat_id>")
            return
        _, _, chat_id_raw = parts
        entity = await event.client.get_entity(chat_id_raw)
        chat_id = entity.id
        user_id = event.sender_id
        async with async_sessionmaker() as session:
            mc = await get_monitored_chat(session, user_id, chat_id)
            if mc is None:
                await event.reply("No monitored chat found.")
                return
        # Enqueue the job (sync RQ call)
        from app.shared.redis_client import get_rq_queue
        rq_queue = get_rq_queue()
        import uuid
        request_id = str(uuid.uuid4())
        from app.userbot.state import store_status_message
        msg = await event.reply("Manual run triggered. Awaiting results...")
        await store_status_message(request_id, msg.id)
        rq_queue.enqueue("app.worker.tasks.process_monitored_chat", mc.id, request_id, True)
    except Exception as e:
        await event.reply(f"Failed to start manual run: {e}")