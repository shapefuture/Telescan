# Minimal system smoke test to ensure all components import and basic config/env works

import os
import pytest

def test_env_vars_present():
    # Check that critical env vars (from .env or environment) are set
    for key in [
        "DATABASE_URL",
        "REDIS_URL",
        "TELEGRAM_API_ID",
        "TELEGRAM_API_HASH",
        "LLM_API_KEY",
    ]:
        assert os.environ.get(key), f"Missing required env var: {key}"

def test_imports():
    # Imports all main modules to catch import errors
    import app.shared.db_models
    import app.shared.db_crud
    import app.shared.database
    import app.shared.redis_client
    import app.userbot.client
    import app.userbot.handlers
    import app.userbot.state
    import app.userbot.ui
    import app.worker.llm_service
    import app.worker.text_cleaner
    import app.worker.tdl_executor
    import app.worker.tasks

@pytest.mark.asyncio
async def test_db_session():
    from app.shared.database import async_sessionmaker
    async with async_sessionmaker() as session:
        assert session