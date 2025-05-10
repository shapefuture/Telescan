from telethon import TelegramClient, events
from config import settings
from app.userbot import handlers

client = TelegramClient(
    settings.TELEGRAM_SESSION_PATH,
    settings.TELEGRAM_API_ID,
    settings.TELEGRAM_API_HASH
)

def register_handlers():
    @client.on(events.NewMessage(pattern=r"^/monitor add"))
    async def _(event):
        await handlers.handle_monitor_add(event)

    @client.on(events.NewMessage(pattern=r"^/monitor list$"))
    async def _(event):
        await handlers.handle_monitor_list(event)

    @client.on(events.NewMessage(pattern=r"^/monitor remove"))
    async def _(event):
        await handlers.handle_monitor_remove(event)

    @client.on(events.NewMessage(pattern=r"^/monitor prompt"))
    async def _(event):
        await handlers.handle_monitor_prompt(event)

    @client.on(events.NewMessage(pattern=r"^/monitor run"))
    async def _(event):
        await handlers.handle_monitor_run(event)