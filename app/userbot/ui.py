# Utilities for building Telegram keyboard layouts and formatting messages

def format_monitored_chats_list(chats):
    """Format a list of monitored chats as a Telegram message."""
    if not chats:
        return "No monitored chats."
    return "\n".join([f"• <b>{c.chat_title}</b> (<code>{c.chat_id}</code>)" for c in chats])
    
async def update_manual_run_status_message(client, request_id: str, status: str):
    """Edits the status message with current progress (if manual run)."""
    from app.userbot.state import get_status_message
    msg_id = await get_status_message(request_id)
    if not msg_id:
        return
    # For demo: Edit message to show status
    await client.edit_message("me", msg_id, f"Status: {status}")