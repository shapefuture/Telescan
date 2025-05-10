# Responsible for sending result messages/files back to the user via Telethon

import os

async def send_llm_insight_and_files(client, user_id, chat_title, summary_path, participants_file_path):
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = f.read()
    msg = f"💡 Summary for {chat_title}:\n\n{summary[:4096]}"
    await client.send_message(user_id, msg)
    if participants_file_path and os.path.exists(participants_file_path):
        await client.send_file(user_id, participants_file_path, caption="Participants list")
        os.remove(participants_file_path)

async def send_failure_insight_message(client, user_id, chat_title, error_message):
    await client.send_message(user_id, f"❌ Failed to process {chat_title}: {error_message}")