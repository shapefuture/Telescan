# Entrypoint for RQ worker service

from rq import Worker
from app.shared.redis_client import get_redis_sync
import app.worker.tasks

def main():
    redis_conn = get_redis_sync()
    worker = Worker(["default"], connection=redis_conn)
    print("RQ Worker starting...")
    worker.work()

if __name__ == "__main__":
    main()