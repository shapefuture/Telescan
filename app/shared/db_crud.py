import logging
from datetime import datetime
from typing import Optional, List, Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.shared.db_models import MonitoredChat, UserSettings

logger = logging.getLogger(__name__)

# --- MonitoredChat CRUD ---

async def add_monitored_chat(
    session: AsyncSession,
    user_id: int,
    chat_id: int,
    chat_title: str,
    prompt: str,
    last_processed_message_id: Optional[int] = None,
    is_active: bool = True,
) -> MonitoredChat:
    """
    Add a new MonitoredChat to the database.
    """
    logger.info(f"Adding monitored chat: user_id={user_id}, chat_id={chat_id}, title={chat_title}")
    mc = MonitoredChat(
        user_id=user_id,
        chat_id=chat_id,
        chat_title=chat_title,
        prompt=prompt,
        last_processed_message_id=last_processed_message_id,
        is_active=is_active,
    )
    try:
        session.add(mc)
        await session.commit()
        await session.refresh(mc)
        logger.info(f"Monitored chat added with id={mc.id}")
        return mc
    except IntegrityError as e:
        logger.error(f"Integrity error adding monitored chat: {e}")
        await session.rollback()
        raise
    except Exception as e:
        logger.exception(f"Unexpected error adding monitored chat: {e}")
        await session.rollback()
        raise

async def get_monitored_chat(session: AsyncSession, user_id: int, chat_id: int) -> Optional[MonitoredChat]:
    """
    Retrieve a single monitored chat for a given user and chat.
    """
    logger.debug(f"Getting monitored chat for user_id={user_id}, chat_id={chat_id}")
    try:
        stmt = select(MonitoredChat).where(
            MonitoredChat.user_id == user_id,
            MonitoredChat.chat_id == chat_id,
        )
        result = await session.execute(stmt)
        mc = result.scalar_one_or_none()
        logger.debug(f"Found monitored chat: {mc}")
        return mc
    except SQLAlchemyError as e:
        logger.error(f"DB error in get_monitored_chat: {e}")
        return None

async def get_all_monitored_chats_for_user(session: AsyncSession, user_id: int) -> List[MonitoredChat]:
    """
    Retrieve all monitored chats for a user.
    """
    logger.debug(f"Getting all monitored chats for user_id={user_id}")
    try:
        stmt = select(MonitoredChat).where(MonitoredChat.user_id == user_id)
        result = await session.execute(stmt)
        chats = result.scalars().all()
        logger.debug(f"Found {len(chats)} monitored chats for user_id={user_id}")
        return chats
    except SQLAlchemyError as e:
        logger.error(f"DB error in get_all_monitored_chats_for_user: {e}")
        return []

async def remove_monitored_chat(session: AsyncSession, user_id: int, chat_id: int) -> int:
    """
    Remove a monitored chat from the database.
    """
    logger.info(f"Removing monitored chat for user_id={user_id}, chat_id={chat_id}")
    try:
        stmt = delete(MonitoredChat).where(
            MonitoredChat.user_id == user_id,
            MonitoredChat.chat_id == chat_id,
        )
        result = await session.execute(stmt)
        await session.commit()
        logger.info(f"Removed {result.rowcount} monitored chat(s)")
        return result.rowcount if hasattr(result, "rowcount") else (result.rowcount() if callable(result.rowcount) else 0)
    except SQLAlchemyError as e:
        logger.error(f"DB error in remove_monitored_chat: {e}")
        await session.rollback()
        return 0

async def update_monitored_chat_prompt(session: AsyncSession, user_id: int, chat_id: int, new_prompt: str) -> int:
    """
    Update the prompt for a monitored chat.
    """
    logger.info(f"Updating prompt for user_id={user_id}, chat_id={chat_id}")
    try:
        stmt = (
            update(MonitoredChat)
            .where(MonitoredChat.user_id == user_id, MonitoredChat.chat_id == chat_id)
            .values(prompt=new_prompt)
        )
        result = await session.execute(stmt)
        await session.commit()
        logger.info(f"Updated prompt for {result.rowcount} chat(s)")
        return result.rowcount
    except SQLAlchemyError as e:
        logger.error(f"DB error in update_monitored_chat_prompt: {e}")
        await session.rollback()
        return 0

async def set_chat_active(session: AsyncSession, user_id: int, chat_id: int, is_active: bool) -> int:
    """
    Set the is_active flag for a monitored chat.
    """
    logger.info(f"Setting chat active={is_active} for user_id={user_id}, chat_id={chat_id}")
    try:
        stmt = (
            update(MonitoredChat)
            .where(MonitoredChat.user_id == user_id, MonitoredChat.chat_id == chat_id)
            .values(is_active=is_active)
        )
        result = await session.execute(stmt)
        await session.commit()
        logger.info(f"Set is_active={is_active} for {result.rowcount} chat(s)")
        return result.rowcount
    except SQLAlchemyError as e:
        logger.error(f"DB error in set_chat_active: {e}")
        await session.rollback()
        return 0

async def get_latest_run_status(session: AsyncSession, user_id: int) -> List[Any]:
    """
    Dummy: Return last processed_message_id for each chat.
    """
    logger.debug(f"Getting latest run status for user_id={user_id}")
    try:
        stmt = select(MonitoredChat.chat_id, MonitoredChat.chat_title, MonitoredChat.last_processed_message_id).where(
            MonitoredChat.user_id == user_id
        )
        result = await session.execute(stmt)
        rows = result.all()
        logger.debug(f"Status rows for user: {rows}")
        return rows
    except SQLAlchemyError as e:
        logger.error(f"DB error in get_latest_run_status: {e}")
        return []

# --- UserSettings CRUD ---

async def set_default_prompt(session: AsyncSession, user_id: int, prompt: str) -> None:
    """
    Set or update the user's default prompt in UserSettings.
    """
    from app.shared.db_models import UserSettings
    logger.info(f"Setting default prompt for user_id={user_id}")
    stmt = select(UserSettings).where(UserSettings.user_id == user_id)
    result = await session.execute(stmt)
    found = result.scalar_one_or_none()
    if found:
        found.default_prompt = prompt
    else:
        us = UserSettings(user_id=user_id, default_prompt=prompt)
        session.add(us)
    try:
        await session.commit()
        logger.info(f"Set default prompt for user_id={user_id}")
    except IntegrityError as e:
        logger.error(f"Integrity error in set_default_prompt: {e}")
        await session.rollback()
        raise

async def get_default_prompt(session: AsyncSession, user_id: int) -> Optional[str]:
    """
    Get a user's default prompt from UserSettings.
    """
    from app.shared.db_models import UserSettings
    logger.debug(f"Getting default prompt for user_id={user_id}")
    stmt = select(UserSettings.default_prompt).where(UserSettings.user_id == user_id)
    result = await session.execute(stmt)
    row = result.first()
    logger.debug(f"Default prompt for user_id={user_id}: {row[0] if row else None}")
    return row[0] if row else None

# --- JobStatus CRUD ---

async def create_job_status(
    session: AsyncSession,
    request_id: str,
    user_id: int,
    chat_id: int,
    chat_title: str,
    status: str,
    detail: Optional[str] = None,
) -> None:
    """
    Create a new JobStatus entry.
    """
    from app.shared.db_models import JobStatus
    logger.info(f"Creating job status: request_id={request_id}, user_id={user_id}, chat_id={chat_id}, status={status}")
    job = JobStatus(
        request_id=request_id,
        user_id=user_id,
        chat_id=chat_id,
        chat_title=chat_title,
        status=status,
        detail=detail,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    try:
        session.add(job)
        await session.commit()
        logger.info(f"Job status created: request_id={request_id}")
    except Exception as e:
        logger.error(f"Error creating job status: {e}")
        await session.rollback()
        raise

async def update_job_status(
    session: AsyncSession,
    request_id: str,
    status: str,
    detail: Optional[str] = None,
) -> None:
    """
    Update the status and detail of a job.
    """
    from app.shared.db_models import JobStatus
    logger.info(f"Updating job status: request_id={request_id}, status={status}")
    try:
        stmt = select(JobStatus).where(JobStatus.request_id == request_id)
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()
        if job:
            job.status = status
            job.detail = detail
            job.updated_at = datetime.utcnow()
            await session.commit()
            logger.info(f"Job status updated: request_id={request_id}")
    except Exception as e:
        logger.error(f"Error updating job status: {e}")
        await session.rollback()
        raise

async def get_job_status(session: AsyncSession, request_id: str) -> Optional[Any]:
    """
    Retrieve a JobStatus entry by request_id.
    """
    from app.shared.db_models import JobStatus
    logger.debug(f"Getting job status for request_id={request_id}")
    try:
        stmt = select(JobStatus).where(JobStatus.request_id == request_id)
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()
        logger.debug(f"Job status: {job}")
        return job
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        return None

async def get_recent_jobs_for_user(session: AsyncSession, user_id: int, limit: int = 10) -> List[Any]:
    """
    Retrieve recent job statuses for a user.
    """
    from app.shared.db_models import JobStatus
    logger.debug(f"Getting recent jobs for user_id={user_id}, limit={limit}")
    try:
        stmt = select(JobStatus).where(JobStatus.user_id == user_id).order_by(JobStatus.created_at.desc()).limit(limit)
        result = await session.execute(stmt)
        jobs = result.scalars().all()
        logger.debug(f"Found {len(jobs)} jobs for user_id={user_id}")
        return jobs
    except Exception as e:
        logger.error(f"Error getting recent jobs: {e}")
        return []
