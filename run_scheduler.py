# Entrypoint for RQ scheduler service

import time
from app.shared.redis_client import get_rq_queue
from app.worker.tasks import periodic_monitoring_check

def main():
    print("RQ Scheduler started (demo polling loop).")
    while True:
        # For demo: schedule periodic_monitoring_check for all users (should be replaced with real schedule/cron)
        # get all unique user_ids from monitored_chats
        # For now, just print
        print("Periodic check (should enqueue jobs for all users)")
        time.sleep(3600)  # Run every hour

if __name__ == "__main__":
    main()