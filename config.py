from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    TELEGRAM_SESSION_PATH: str = "/data/telethon.session"
    TDL_CONFIG_DIR: str = "/data/.tdl"
    TDL_OUTPUT_DIR_BASE: str = "/data/tdl_output"
    LLM_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()