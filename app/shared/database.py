# Async SQLAlchemy engine/session setup

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)