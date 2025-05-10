# LLM API interaction

import httpx
from config import settings

async def get_llm_summary(history_text: str, prompt: str, max_tokens: int = 2048) -> str:
    """Call LLM API and return summary (raise Exception on failure)."""
    url = getattr(settings, "LLM_ENDPOINT_URL", None) or "https://api.openai.com/v1/chat/completions"
    api_key = settings.LLM_API_KEY
    # For OpenAI-compatible APIs
    # Truncate history if exceeds model context
    max_chars = 8000
    truncated_history = history_text[-max_chars:] if len(history_text) > max_chars else history_text
    payload = {
        "model": getattr(settings, "LLM_MODEL_NAME", "gpt-3.5-turbo"),
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
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]