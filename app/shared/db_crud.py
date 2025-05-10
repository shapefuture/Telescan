# CRUD operations for Supabase/Postgres via SQLAlchemy

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.db_models import MonitoredChat

async def add_monitored_chat(
    session: AsyncSession,
    user_id: int,
    chat_id: int,
    chat_title: str,
    prompt: str,
    last_processed_message_id: int = None,
    is_active: bool = True,
) -> MonitoredChat:
    mc = MonitoredChat(
        user_id=user_id,
        chat_id=chat_id,
        chat_title=chat_title,
        prompt=prompt,
        last_processed_message_id=last_processed_message_id,
        is_active=is_active,
    )
    session.add(mc)
    await session.commit()
    await session.refresh(mc)
    return mc

async def get_monitored_chat(session: AsyncSession, user_id: int, chat_id: int) -> MonitoredChat | None:
    stmt = select(MonitoredChat).where(
        MonitoredChat.user_id == user_id,
        MonitoredChat.chat_id == chat_id,
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_all_monitored_chats_for_user(session: AsyncSession, user_id: int) -> list[MonitoredChat]:
    stmt = select(MonitoredChat).where(MonitoredChat.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def remove_monitored_chat(session: AsyncSession, user_id: int, chat_id: int) -> int:
    stmt = delete(MonitoredChat).where(
        MonitoredChat.user_id == user_id,
        MonitoredChat.chat_id == chat_id,
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount if hasattr(result, "rowcount") else (result.rowcount() if callable(result.rowcount) else 0)

async def update_monitored_chat_prompt(session: AsyncSession, user_id: int, chat_id: int, new_prompt: str) -> int:
    stmt = (
        update(MonitoredChat)
        .where(MonitoredChat.user_id == user_id, MonitoredChat.chat_id == chat_id)
        .values(prompt=new_prompt)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount