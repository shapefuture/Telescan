# RQ worker task definitions

import asyncio
from app.shared.database import async_sessionmaker
from app.shared.db_crud import get_monitored_chat, update_monitored_chat_prompt
from app.shared.db_crud import get_all_monitored_chats_for_user
from app.worker.tdl_executor import execute_tdl_command, TdlExecutionError
from app.worker.text_cleaner import clean_tdl_message_text
from app.worker.llm_service import get_llm_summary
from app.shared.redis_client import get_redis_sync
import os
import json

def _publish_status(request_id, status, detail=None):
    redis = get_redis_sync()
    key = f"request_status:{request_id}"
    payload = {"status": status}
    if detail is not None:
        payload["detail"] = detail
    redis.publish(key, json.dumps(payload))

def process_monitored_chat(monitored_chat_db_id, request_id=None, is_manual_run=False):
    """Main worker task: run tdl, clean text, call LLM, publish status"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_process(monitored_chat_db_id, request_id, is_manual_run))

async def _process(monitored_chat_db_id, request_id, is_manual_run):
    from app.shared.db_models import MonitoredChat
    from config import settings

    async with async_sessionmaker() as session:
        mc = await session.get(MonitoredChat, monitored_chat_db_id)
        if not mc:
            _publish_status(request_id, "FAILED", {"error": "MonitoredChat not found"})
            return
        _publish_status(request_id, "STARTED")
        output_dir = os.path.join(settings.TDL_OUTPUT_DIR_BASE, f"chat_{mc.chat_id}")
        os.makedirs(output_dir, exist_ok=True)
        history_json_path = os.path.join(output_dir, "history.json")
        participants_json_path = os.path.join(output_dir, "participants.json")
        # Step 1: History export
        history_args = ["chat", "export", "-c", str(mc.chat_id), "--all", "-o", history_json_path]
        try:
            _publish_status(request_id, "TDL_HISTORY_EXPORT")
            await execute_tdl_command(history_args)
        except Exception as e:
            _publish_status(request_id, "FAILED", {"error": f"tdl export failed: {e}", "user_id": mc.user_id, "chat_id": mc.chat_id, "chat_title": mc.chat_title})
            return
        # Step 2: Clean messages
        with open(history_json_path, "r", encoding="utf-8") as f:
            history_data = json.load(f)
        cleaned_lines = []
        for msg in history_data.get("messages", []):
            cleaned = clean_tdl_message_text(msg)
            if cleaned:
                cleaned_lines.append(cleaned)
        cleaned_history = "\n".join(cleaned_lines)
        cleaned_txt_path = os.path.join(output_dir, "history_cleaned.txt")
        with open(cleaned_txt_path, "w", encoding="utf-8") as f:
            f.write(cleaned_history)
        # Step 3: Participants export (optional)
        try:
            _publish_status(request_id, "TDL_PARTICIPANTS_EXPORT")
            await execute_tdl_command(["chat", "users", "-c", str(mc.chat_id), "-o", participants_json_path])
            with open(participants_json_path, "r", encoding="utf-8") as f:
                participants_data = json.load(f)
            participants_txt_path = os.path.join(output_dir, "participants.txt")
            with open(participants_txt_path, "w", encoding="utf-8") as f2:
                for user in participants_data.get("users", []):
                    line = f"{user.get('id')} {user.get('username') or ''} {user.get('first_name') or ''} {user.get('last_name') or ''}\n"
                    f2.write(line)
        except Exception as e:
            participants_txt_path = None
            _publish_status(request_id, "TDL_PARTICIPANTS_EXPORT_FAILED", {"error": str(e)})

        # Step 4: LLM summarization
        try:
            _publish_status(request_id, "CALLING_LLM")
            summary = await get_llm_summary(cleaned_history, mc.prompt)
            summary_txt_path = os.path.join(output_dir, "summary.txt")
            with open(summary_txt_path, "w", encoding="utf-8") as fs:
                fs.write(summary)
        except Exception as e:
            _publish_status(request_id, "FAILED", {
                "error": f"LLM failed: {e}",
                "user_id": mc.user_id,
                "chat_id": mc.chat_id,
                "chat_title": mc.chat_title
            })
            return

        # Step 5: Success - publish all paths and metadata
        _publish_status(request_id, "SUCCESS", {
            "user_id": mc.user_id,
            "chat_id": mc.chat_id,
            "chat_title": mc.chat_title,
            "summary_path": summary_txt_path,
            "participants_path": participants_txt_path,
            "history_path": cleaned_txt_path,
        })

def periodic_monitoring_check(user_telegram_id):
    """Scheduled check for due monitored chats for a user."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_periodic_check(user_telegram_id))

async def _periodic_check(user_telegram_id):
    async with async_sessionmaker() as session:
        chats = await get_all_monitored_chats_for_user(session, user_telegram_id)
        # For each active chat, enqueue process_monitored_chat (simulate with print)
        from app.shared.redis_client import get_rq_queue
        rq_queue = get_rq_queue()
        for mc in chats:
            if mc.is_active:
                rq_queue.enqueue("app.worker.tasks.process_monitored_chat", mc.id, is_manual_run=False)