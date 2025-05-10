# Entrypoint for RQ scheduler service

import asyncio
import time
from app.shared.database import async_sessionmaker
from app.shared.db_models import MonitoredChat
from app.worker.tasks import periodic_monitoring_check

def main():
    print("RQ Scheduler started. Will periodically trigger periodic_monitoring_check for all users with monitored chats.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scheduler_loop())

async def scheduler_loop():
    while True:
        async with async_sessionmaker() as session:
            # Get all distinct user_ids with active monitored chats
            users = await session.execute(
                "SELECT DISTINCT user_id FROM monitored_chats WHERE is_active = true"
            )
            user_ids = [row[0] for row in users.fetchall()]
            print(f"Scheduler: Found {len(user_ids)} monitored users.")
            for user_id in user_ids:
                try:
                    # This will enqueue jobs for all monitored chats for the user
                    periodic_monitoring_check(user_id)
                except Exception as e:
                    print(f"Error scheduling for user {user_id}: {e}")
        await asyncio.sleep(3600)  # Run every hour

if __name__ == "__main__":
    main()