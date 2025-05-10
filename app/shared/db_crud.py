from datetime import datetime

# ... previous code ...

async def create_job_status(
    session: AsyncSession,
    request_id: str,
    user_id: int,
    chat_id: int,
    chat_title: str,
    status: str,
    detail: str | None = None,
) -> None:
    from app.shared.db_models import JobStatus
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
    session.add(job)
    await session.commit()

async def update_job_status(
    session: AsyncSession,
    request_id: str,
    status: str,
    detail: str | None = None,
) -> None:
    from app.shared.db_models import JobStatus
    stmt = select(JobStatus).where(JobStatus.request_id == request_id)
    result = await session.execute(stmt)
    job = result.scalar_one_or_none()
    if job:
        job.status = status
        job.detail = detail
        job.updated_at = datetime.utcnow()
        await session.commit()

async def get_job_status(session: AsyncSession, request_id: str):
    from app.shared.db_models import JobStatus
    stmt = select(JobStatus).where(JobStatus.request_id == request_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_recent_jobs_for_user(session: AsyncSession, user_id: int, limit: int = 10):
    from app.shared.db_models import JobStatus
    stmt = select(JobStatus).where(JobStatus.user_id == user_id).order_by(JobStatus.created_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()
