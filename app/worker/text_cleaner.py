# Text cleaning utilities

def clean_tdl_message_text(message_obj):
    # TODO: Apply cleaning (remove system messages, urls, etc.)
    return message_obj.get("text", "")