# Listens to Redis Pub/Sub for job completion or progress events

import asyncio
import json
from app.shared.redis_client import get_redis_async
from app.userbot.results_sender import send_llm_insight_and_files, send_failure_insight_message
from app.userbot.state import get_status_message

async def listen_for_job_events(client, settings):
    redis = get_redis_async()
    pubsub = redis.pubsub()
    await pubsub.psubscribe("request_status:*")
    async for msg in pubsub.listen():
        if msg["type"] == "pmessage":
            data = json.loads(msg["data"])
            status = data.get("status")
            detail = data.get("detail")
            key = msg["channel"]
            request_id = key.split(":")[-1]
            if status == "SUCCESS":
                await handle_insight_job_completion(client, request_id, detail)
            elif status == "FAILED":
                await handle_insight_job_completion(client, request_id, detail, failed=True)
            # else: update status message etc.

async def handle_insight_job_completion(client, request_id, detail, failed=False):
    msg_id = await get_status_message(request_id)
    # For demo, assume user_id/chat_title are part of detail
    if failed:
        await send_failure_insight_message(client, detail.get("user_id"), detail.get("chat_title"), detail.get("detail"))
    else:
        await send_llm_insight_and_files(
            client,
            detail.get("user_id"),
            detail.get("chat_title"),
            detail.get("summary_path"),
            detail.get("participants_path"),
        )