# SQLAlchemy models for Supabase/Postgres

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Boolean, Text, Integer

class Base(AsyncAttrs, DeclarativeBase):
    pass

class MonitoredChat(Base):
    __tablename__ = "monitored_chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)  # Telegram user id
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)  # Telegram chat id
    chat_title: Mapped[str] = mapped_column(String(256))
    prompt: Mapped[str] = mapped_column(Text)
    last_processed_message_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

# Engine/session setup will be in a separate database.py