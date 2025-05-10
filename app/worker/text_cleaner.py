# Text cleaning utilities

import re
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("telegram_insight_agent.text_cleaner")

def clean_tdl_message_text(message_obj: Dict[str, Any]) -> Optional[str]:
    """
    Clean a Telegram message dict from tdl export for summarization.

    Removes system/service messages, URLs, user mentions, media placeholders, and excess whitespace.
    Skips short or empty results.

    Args:
        message_obj: A tdl message dict.

    Returns:
        Cleaned string, or None if unsuitable.
    """
    try:
        text = message_obj.get("text", "")
        logger.debug(f"Cleaning message: {text!r}")
        if not text or not isinstance(text, str):
            logger.debug("No text in message or not a string")
            return None
        # Remove system messages or service types
        if message_obj.get("service"):
            logger.debug("Skipping system/service message")
            return None
        # Remove URLs
        text = re.sub(r"https?://\S+", "", text)
        # Remove user mentions ("@username")
        text = re.sub(r"@\w+", "", text)
        # Remove media placeholder
        text = re.sub(r"\u2063", "", text)
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
        # Skip very short or empty results
        if len(text) < 3:
            logger.debug("Message too short after cleaning")
            return None
        logger.debug(f"Cleaned message: {text!r}")
        return text
    except Exception as e:
        logger.exception(f"Error cleaning message: {e}, message_obj={message_obj}")
        return None

# --- Pytest skeleton ---

"""
import pytest
from app.worker.text_cleaner import clean_tdl_message_text

def test_clean_url_removal():
    msg = {"text": "Check this https://example.com"}
    assert clean_tdl_message_text(msg) == "Check this"

def test_clean_mentions():
    msg = {"text": "@user hello"}
    assert clean_tdl_message_text(msg) == "hello"

def test_service_message_skipped():
    msg = {"service": True, "text": "User joined"}
    assert clean_tdl_message_text(msg) is None

def test_empty_message():
    msg = {"text": ""}
    assert clean_tdl_message_text(msg) is None

def test_short_message():
    msg = {"text": "ok"}
    assert clean_tdl_message_text(msg) is None

def test_unicode_media_placeholder():
    msg = {"text": "photo\u2063"}
    assert clean_tdl_message_text(msg) == "photo"
"""