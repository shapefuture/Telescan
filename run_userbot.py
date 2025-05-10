"""
Entrypoint for Telethon userbot service for Telegram Insight Agent.
"""

import asyncio
import logging
from typing import NoReturn
from app.userbot.client import client, register_handlers
from app.logging_config import setup_logging
from app.userbot.event_listener import listen_for_job_events
from config import settings

logger = logging.getLogger("telegram_insight_agent.run_userbot")

def main() -> NoReturn:
    """
    Start the Telethon userbot service, including event handlers and Redis job listener.
    """
    setup_logging()
    logger.info("Starting Telethon userbot main routine.")
    register_handlers()
    loop = asyncio.get_event_loop()
    # Start Redis pub/sub for job status (runs forever)
    loop.create_task(listen_for_job_events(client, settings))
    logger.info("Starting Telethon client event loop.")
    try:
        client.loop = loop
        client.start()
        client.run_until_disconnected()
    except KeyboardInterrupt:
        logger.info("Userbot stopped (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"Userbot crashed: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

# --- Pytest skeleton ---

"""
import pytest
from unittest.mock import patch

def test_main_importable():
    import run_userbot
    assert hasattr(run_userbot, "main")
"""