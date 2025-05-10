# Utilities for building Telegram keyboard layouts and formatting messages

def format_monitored_chats_list(chats):
    # TODO: Format a list of monitored chats as a Telegram message
    return "Monitored chats:\n" + "\n".join(f"- {chat['title']} ({chat['id']})" for chat in chats)