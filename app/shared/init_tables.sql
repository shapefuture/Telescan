-- Create monitored_chats table
CREATE TABLE IF NOT EXISTS monitored_chats (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    chat_title VARCHAR(256) NOT NULL,
    prompt TEXT NOT NULL,
    last_processed_message_id BIGINT,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(user_id, chat_id)
);

-- Create user_settings table for per-user default prompt
CREATE TABLE IF NOT EXISTS user_settings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    default_prompt TEXT
);