# Listens to Redis Pub/Sub for job completion or progress events

import asyncio
import json
from app.shared.redis_client import get_redis_async
from app.userbot.results_sender import send_llm_insight_and_files, send_failure_insight_message
from app.userbot.state import get_status_message
from app.shared.database import async_sessionmaker
from app.shared.db_models import MonitoredChat

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
                await handle_insight_job_completion(client, request_id, detail, failed=False)
            elif status == "FAILED":
                await handle_insight_job_completion(client, request_id, detail, failed=True)
            elif status in ("TDL_HISTORY_EXPORT", "TDL_PARTICIPANTS_EXPORT", "CALLING_LLM"):
                await update_manual_run_status_message(client, request_id, status)
            elif status == "TDL_PARTICIPANTS_EXPORT_FAILED":
                await update_manual_run_status_message(client, request_id, "Participants export failed")

async def handle_insight_job_completion(client, request_id, detail, failed=False):
    # detail from worker: should include user_id, chat_id, chat_title, summary_path, participants_path, error, etc.
    msg_id = await get_status_message(request_id)
    user_id = detail.get("user_id")
    chat_title = detail.get("chat_title")
    if failed:
        await send_failure_insight_message(client, user_id, chat_title, str(detail))
    else:
        await send_llm_insight_and_files(
            client,
            user_id,
            chat_title,
            detail.get("summary_path"),
            detail.get("participants_path"),
        )