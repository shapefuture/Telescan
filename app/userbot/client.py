from telethon import TelegramClient
from config import settings

client = TelegramClient(
    settings.TELEGRAM_SESSION_PATH,
    settings.TELEGRAM_API_ID,
    settings.TELEGRAM_API_HASH
)