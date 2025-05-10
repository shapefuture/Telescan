# Script to initialize the database (create all tables)

import asyncio
from app.shared.db_models import Base
from app.shared.database import engine

async def init_db():
    async with engine.begin() as conn:
        # This will create all tables defined in db_models.py (MonitoredChat, UserSettings, etc.)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created (MonitoredChat, UserSettings).")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created (including user_settings and job_status).")

if __name__ == "__main__":
    asyncio.run(init_db())