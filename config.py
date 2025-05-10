"""
Configuration (env/Pydantic) for Telegram Insight Agent.
"""

import logging
from pydantic import BaseSettings, ValidationError

logger = logging.getLogger("telegram_insight_agent.config")

class Settings(BaseSettings):
    """
    App config loaded from environment variables.
    """
    DATABASE_URL: str
    REDIS_URL: str
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    TELEGRAM_SESSION_PATH: str
    TDL_CONFIG_DIR: str
    TDL_OUTPUT_DIR_BASE: str
    LLM_API_KEY: str
    LLM_ENDPOINT_URL: str = "https://api.openai.com/v1/chat/completions"
    LLM_MODEL_NAME: str = "gpt-3.5-turbo"

try:
    settings = Settings()
    logger.info("App config loaded successfully.")
except ValidationError as e:
    logger.error(f"App config validation failed: {e}")
    raise

# --- Pytest skeleton ---

"""
def test_config_loads(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:pw@localhost:5432/db")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abc")
    monkeypatch.setenv("TELEGRAM_SESSION_PATH", "/tmp/session")
    monkeypatch.setenv("TDL_CONFIG_DIR", "/tmp/tdl")
    monkeypatch.setenv("TDL_OUTPUT_DIR_BASE", "/tmp/tdl_out")
    monkeypatch.setenv("LLM_API_KEY", "sk-...")
    from config import Settings
    s = Settings()
    assert s.DATABASE_URL.startswith("postgresql")
"""