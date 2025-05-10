# Entrypoint for Telethon userbot service

from app.userbot.client import client
from app.logging_config import setup_logging

def main():
    setup_logging()
    # TODO: Register handlers and start Telethon client

if __name__ == "__main__":
    main()