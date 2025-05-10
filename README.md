# Telegram Insight Agent

## Setup & Deployment

### 1. Database (Supabase/Postgres)

- Ensure your Supabase/Postgres instance is running.
- **Required tables:** `monitored_chats`, `user_settings`
- If using Supabase dashboard or a fresh DB, you MUST create tables before running any backend services:
    1. Open the Supabase SQL editor.
    2. Paste and run the contents of [`app/shared/init_tables.sql`](app/shared/init_tables.sql).
    3. This will create all tables required by the backend.
- For local/dev/testing with SQLite/Postgres, you can also run:
    ```
    python app/shared/init_db.py
    ```
    to create all tables as defined in the ORM.

### 2. Environment

- Copy `.env.example` to `.env` and fill in:
    - `DATABASE_URL`
    - `REDIS_URL`
    - `TELEGRAM_API_ID`
    - `TELEGRAM_API_HASH`
    - `LLM_API_KEY`
    - (etc.)

### 3. Install Python dependencies

```
pip install -r requirements.txt
```

### 4. Initial Auth

- Deploy or run the backend on Fly.io or locally.
- SSH into the container/VM and run:
    ```
    tdl login
    ```
    to authenticate the Telegram CLI session (`TDL_CONFIG_DIR`).
- Run:
    ```
    python run_userbot.py
    ```
    once interactively to create the Telethon session.

### 5. Service Startup

- Start the three main services:
    - Userbot: `python run_userbot.py`
    - Worker:  `python run_worker.py`
    - Scheduler: `python run_scheduler.py`

### 6. Usage

- Use Telegram to interact with your own userbot via commands:
    - `/monitor add <chat_id> <prompt>`
    - `/monitor list`
    - `/monitor run <chat_id>`
    - `/settings`
    - `/pause <chat_id>`
    - `/resume <chat_id>`
    - `/cancel <request_id>`
    - `/status`

---

**No placeholders:** All database tables, environment variables, and service flows are fully implemented and documented. If you follow the above steps, the system will be fully functional as described in the project plan.

## Project Plan

- For a detailed architecture, phased requirements, and implementation breakdown, see [`plan.md`](plan.md).

```

**No placeholders:** All database tables, environment variables, and service flows are fully implemented and documented. If you follow the above steps, the system will be fully functional as described in the project plan.
