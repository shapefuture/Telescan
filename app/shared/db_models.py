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

"""
SQLAlchemy ORM models for Telegram Insight Agent.
"""

import logging
from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, Boolean, DateTime, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime

logger = logging.getLogger("telegram_insight_agent.db_models")

Base = declarative_base()

class MonitoredChat(Base):
    """
    Model for monitored Telegram chats.
    """
    __tablename__ = "monitored_chats"
    __table_args__ = (UniqueConstraint("user_id", "chat_id", name="uq_monitored_chats_user_chat"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_title: Mapped[str] = mapped_column(String(256), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    last_processed_message_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return (f"<MonitoredChat(id={self.id}, user_id={self.user_id}, "
                f"chat_id={self.chat_id}, title={self.chat_title})>")

class UserSettings(Base):
    """
    Model for per-user default prompt/settings.
    """
    __tablename__ = "user_settings"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_settings_user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)
    default_prompt: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<UserSettings(user_id={self.user_id}, default_prompt={self.default_prompt!r})>"

class JobStatus(Base):
    """
    Model for status tracking of background jobs (summarization requests).
    """
    __tablename__ = "job_status"
    __table_args__ = (UniqueConstraint("request_id", name="uq_job_status_request_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_title: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (f"<JobStatus(request_id={self.request_id}, user_id={self.user_id}, "
                f"chat_id={self.chat_id}, status={self.status})>")

# --- Pytest skeleton for models ---

"""
import pytest
from app.shared.db_models import Base, MonitoredChat, UserSettings, JobStatus

def test_monitored_chat_schema():
    # Ensure class exists and has expected columns
    cols = [c.name for c in MonitoredChat.__table__.columns]
    assert "user_id" in cols and "chat_id" in cols and "prompt" in cols

def test_user_settings_schema():
    cols = [c.name for c in UserSettings.__table__.columns]
    assert "user_id" in cols and "default_prompt" in cols

def test_job_status_schema():
    cols = [c.name for c in JobStatus.__table__.columns]
    assert "request_id" in cols and "status" in cols and "created_at" in cols
"""

class JobStatus(Base):
    __tablename__ = "job_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_title: Mapped[str] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(String(32))  # e.g. QUEUED, STARTED, RUNNING, SUCCESS, FAILED, CANCELLED
    detail: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)