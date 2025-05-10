# Utilities for building Telegram keyboard layouts and formatting messages

def format_monitored_chats_list(chats):
    """Format a list of monitored chats as a Telegram message."""
    if not chats:
        return "No monitored chats."
    return "Monitored chats:\n" + "\n".join(f"- {c.chat_title} ({c.chat_id})" for c in chats)