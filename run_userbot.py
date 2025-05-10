# Entrypoint for Telethon userbot service

import asyncio
from app.userbot.client import client, register_handlers
from app.logging_config import setup_logging
from app.userbot.event_listener import listen_for_job_events
from config import settings

def main():
    setup_logging()
    register_handlers()
    loop = asyncio.get_event_loop()
    loop.create_task(listen_for_job_events(client, settings))
    print("Starting Telethon userbot...")
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    main()