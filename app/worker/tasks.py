# RQ worker task definitions

def process_monitored_chat(monitored_chat_db_id, request_id=None, is_manual_run=False):
    # TODO: Main worker task: run tdl, clean text, call LLM, publish status
    raise NotImplementedError

def periodic_monitoring_check(user_telegram_id):
    # TODO: Scheduled check for due monitored chats
    pass