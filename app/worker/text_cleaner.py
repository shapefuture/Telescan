# Text cleaning utilities

import re

def clean_tdl_message_text(message_obj: dict) -> str | None:
    text = message_obj.get("text", "")
    if not text or not isinstance(text, str):
        return None
    # Remove system messages or service types
    if message_obj.get("service"):
        return None
    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)
    # Remove user mentions ("@username")
    text = re.sub(r"@\w+", "", text)
    # Remove media placeholder
    text = re.sub(r"\u2063", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Skip very short or empty results
    if len(text) < 3:
        return None
    return text