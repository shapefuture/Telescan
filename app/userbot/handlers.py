# Userbot command/callback handlers

from app.shared.database import async_sessionmaker
from app.shared.db_crud import add_monitored_chat, get_all_monitored_chats_for_user, remove_monitored_chat, update_monitored_chat_prompt
from app.userbot.ui import format_monitored_chats_list
from app.shared.db_crud import get_monitored_chat
from app.worker.tasks import process_monitored_chat
import asyncio

async def handle_monitor_add(event):
    """Usage: /monitor add <chat_id> <prompt>"""
    try:
        # Accept both numeric IDs and @usernames
        parts = event.raw_text.split(maxsplit=3)
        if len(parts) < 4:
            await event.reply("Usage: /monitor add <chat_id> <prompt>")
            return
        _, _, chat_id_raw, prompt = parts
        # Try to resolve chat_id and title using Telethon
        entity = await event.client.get_entity(chat_id_raw)
        chat_id = entity.id
        chat_title = getattr(entity, "title", getattr(entity, "username", str(chat_id)))
        user_id = event.sender_id
        async with async_sessionmaker() as session:
            # Check if already monitored
            existing = await get_monitored_chat(session, user_id, chat_id)
            if existing:
                await event.reply(f"Already monitoring {chat_title} ({chat_id}).")
                return
            mc = await add_monitored_chat(session, user_id, chat_id, chat_title, prompt)
            await event.reply(f"Added monitoring for {chat_title} ({chat_id}).")
    except Exception as e:
        await event.reply(f"Failed to add monitoring: {e}")

async def handle_monitor_list(event):
    user_id = event.sender_id
    async with async_sessionmaker() as session:
        chats = await get_all_monitored_chats_for_user(session, user_id)
        msg = format_monitored_chats_list(chats)
        await event.reply(msg)

async def handle_monitor_remove(event):
    """Usage: /monitor remove <chat_id>"""
    try:
        parts = event.raw_text.split()
        if len(parts) < 3:
            await event.reply("Usage: /monitor remove <chat_id>")
            return
        _, _, chat_id = parts
        chat_id = int(chat_id)
        user_id = event.sender_id
        async with async_sessionmaker() as session:
            rc = await remove_monitored_chat(session, user_id, chat_id)
            await event.reply(f"Removed monitoring for chat {chat_id}.")
    except Exception as e:
        await event.reply(f"Failed to remove monitoring: {e}")

async def handle_monitor_prompt(event):
    """Usage: /monitor prompt <chat_id> <new_prompt>"""
    try:
        parts = event.raw_text.split(maxsplit=3)
        if len(parts) < 4:
            await event.reply("Usage: /monitor prompt <chat_id> <new_prompt>")
            return
        _, _, chat_id, new_prompt = parts
        chat_id = int(chat_id)
        user_id = event.sender_id
        async with async_sessionmaker() as session:
            rc = await update_monitored_chat_prompt(session, user_id, chat_id, new_prompt)
            await event.reply(f"Updated prompt for chat {chat_id}.")
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