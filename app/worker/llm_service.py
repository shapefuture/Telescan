# LLM API interaction

import httpx
import logging
from typing import Optional
from config import settings

logger = logging.getLogger("telegram_insight_agent.llm_service")

async def get_llm_summary(history_text: str, prompt: str, max_tokens: int = 2048) -> str:
    """
    Call LLM API (OpenAI-compatible) and return summary.

    Args:
        history_text: The cleaned chat history to summarize.
        prompt: The LLM prompt.
        max_tokens: Max tokens for LLM output.

    Returns:
        LLM summary as string.

    Raises:
        Exception for HTTP or JSON parsing errors.
    """
    url = getattr(settings, "LLM_ENDPOINT_URL", None) or "https://api.openai.com/v1/chat/completions"
    api_key = settings.LLM_API_KEY
    model = getattr(settings, "LLM_MODEL_NAME", "gpt-3.5-turbo")
    max_chars = 8000
    truncated_history = history_text[-max_chars:] if len(history_text) > max_chars else history_text
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": truncated_history}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    logger.info(f"Requesting LLM summary with model={model}, tokens={max_tokens}")
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)
            logger.debug(f"LLM API response code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.debug(f"LLM API response body: {data}")
            # OpenAI format: choices[0].message.content
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        logger.error(f"LLM API HTTP error: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.exception(f"LLM API call failed: {e}")
        raise

# --- Test skeleton for get_llm_summary ---

"""
import pytest
from app.worker.llm_service import get_llm_summary

@pytest.mark.asyncio
async def test_llm_success(monkeypatch):
    # monkeypatch httpx.AsyncClient.post to return a mock response with .json()
    pass

@pytest.mark.asyncio
async def test_llm_http_error(monkeypatch):
    # Simulate httpx.HTTPStatusError
    pass

@pytest.mark.asyncio
async def test_llm_json_error(monkeypatch):
    # Simulate invalid JSON in response
    pass
"""