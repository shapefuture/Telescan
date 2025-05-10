# Project: Cloud-Hosted Telegram Insight Agent (v8.0 - tdl-Powered Userbot)

**Goal:** Develop a secure, robust, scalable userbot service hosted on Fly.io, using Supabase for data persistence. The service, acting on behalf of the user's Telegram account, interacts via Telegram commands/buttons. It allows the user to manage monitored chats, provide prompts, triggers background extraction (via `tdl` CLI) and LLM processing via RQ/Redis, provides real-time progress updates via Telegram, and delivers insights/results as messages/files back in Telegram.

**Architecture:**
1.  **Telegram "Bot" Interface (User Account acting via Telethon):** This is the `userbot_service.py` running on Fly.io. It listens to your own incoming messages/callbacks.
2.  **Telegram Engine:** `tdl` executable (installed in the Fly.io Docker image).
3.  **Task Orchestration (within Userbot Service & RQ Tasks):**
    *   Userbot service determines *what* `tdl` commands to run.
    *   RQ tasks *execute* these `tdl` commands as subprocesses.
4.  **Task Queue:** RQ + Redis (Redis as Fly App or external).
5.  **RQ Workers (Fly.io):** Python processes that execute the RQ tasks (which in turn run `tdl`).
6.  **Database:** Supabase PostgreSQL (for monitored chats, job status, user settings).
7.  **Persistent Storage (Fly Volume):** For `tdl` config/session, intermediate `tdl` JSON output, final cleaned TXT files before upload.
8.  **LLM Interaction:** `httpx` from RQ worker.

**User Flow (Simplified):**
1.  **(Dev Setup):** Deploy to Fly.io. Run `tdl login` *once* via `fly ssh console` in the `userbot_service` container to authenticate `tdl`. Run `run_userbot.py` interactively *once* in the `userbot_service` container for Telethon's initial auth (creating its `.session` file).
2.  **(User Interaction - All via Telegram):**
    a.  User sends `/monitor add @channelname daily Summarize key topics` to their own "Saved Messages" (or a dedicated control chat).
    b.  Userbot Service (`userbot_app.py` via Telethon) receives this, parses it, saves to Supabase.
    c.  Scheduled job (or manual `/monitor run @channelname`) triggers an RQ task.
    d.  RQ Worker task:
        i.  Retrieves info from Supabase.
        ii. Executes `tdl chat export -c @channelname --min-id <last_id> -o ...json` as subprocess.
        iii. Executes `tdl chat users ...` (if group).
        iv. Parses JSONs, cleans text.
        v.  Calls LLM API with text and prompt.
        vi. Publishes "SUCCESS/FAILURE + summary/error" to Redis Pub/Sub.
    e.  Userbot Service (listening to Pub/Sub): Receives event, formats insight, sends to user as Telegram message. Updates `last_processed_id` in Supabase.

**Technology Stack:** (Same as v5.2: Python, Telethon, RQ, Redis, Supabase/Postgres, `tdl`, `httpx`, Pydantic, etc.)

**Project Structure:** (Same as v5.2, `tdl_orchestrator.py` might be part of `worker/tasks.py` or a util)

/telegram-userbot-tdl
|-- Dockerfile             # Installs Python, tdl, copies app
|-- fly.toml
|-- run_userbot.py         # Entry for Telethon userbot service
|-- run_worker.py          # Entry for RQ worker service
|-- run_scheduler.py       # Entry for RQ scheduler service
|-- requirements.txt
|-- config.py
|-- .env
|-- .gitignore
|-- implementation_plan.md
|-- /app
|   |-- __init__.py
|   |-- userbot            # Telethon Userbot specific logic
|   |   |-- client.py      # Telethon client init
|   |   |-- handlers.py    # Command/Callback handlers
|   |   |-- ui.py          # Keyboard builders, message formatters
|   |   |-- state.py       # Manages temp interactive state (e.g., for multi-step commands) via Redis
|   |   |-- event_listener.py # Listens to Redis Pub/Sub for job completions
|   |   |-- results_sender.py # Sends final insights/files via Telethon
|   |-- worker             # RQ Worker logic
|   |   |-- __init__.py
|   |   |-- tasks.py       # RQ task definitions (orchestrates tdl, calls LLM)
|   |   |-- tdl_executor.py # NEW/Refined: Robustly executes tdl commands & parses output
|   |   |-- text_cleaner.py # Text cleaning utilities
|   |   |-- llm_service.py # LLM API interaction
|   |-- shared             # Shared components
|   |   |-- __init__.py
|   |   |-- redis_client.py # Redis connection & RQ Queue setup
|   |   |-- db_models.py   # SQLAlchemy models for Supabase
|   |   |-- db_crud.py     # CRUD operations for Supabase
|   |-- logging_config.py
|-- /tests
# ... (test structure mirrors app structure) ...

---
**AI Implementation Best Practices Checklist (MANDATORY for each step):**
*   **(All previous best practices apply - Style, Typing, Modularity, Config, Security, Error Handling, Logging, Testing, Docs, Dependencies)**
*   **[ ] `tdl` Execution:** All `tdl` calls within RQ tasks must be via a robust helper function in `app/worker/tdl_executor.py`. This helper must use `subprocess.run` or `subprocess.Popen` carefully, capture `stdout`/`stderr`, check exit codes, handle timeouts, and parse expected JSON output safely. Ensure `tdl` uses a persistent config directory (`--config /data/.tdl`).
*   **[ ] Telethon as Controller:** The `userbot_app.py` is the user-facing controller. It parses Telegram messages, manages minimal interactive state (e.g., waiting for a follow-up message for a multi-part command) using Redis, updates the Supabase DB for persistent subscriptions, and enqueues jobs to RQ. It *does not* run `tdl` directly.
*   **[ ] Clear API between Components:** Userbot enqueues task with all necessary data (`chat_id`, `prompt`, `last_message_id`). Worker task returns structured data (summary, error, file paths). Pub/Sub messages are structured (JSON).
*   **[ ] Supabase CRUD:** All database interactions via `app/shared/db_crud.py` using SQLAlchemy async sessions.

---

## Phase 1: Foundation, Config, DB, `tdl` Setup, Fly.io Base

**Goal:** Set up project, robust config, Supabase DB models/CRUD, logging, Redis, basic Telethon userbot that connects, basic RQ worker that can be started, and deployable Fly.io app with `tdl` installed in the image.

**Steps:**

1.  `[v]` Project Setup: Structure, Git, venv.
2.  `[ ]` Supabase Project Setup: Get connection string.
3.  `[ ]` Dependencies (`requirements.txt`): Add `asyncpg`, `SQLAlchemy[asyncio]`.
4.  `[ ]` Configuration (`config.py`, `.env`): Pydantic `Settings` for `DATABASE_URL`, `REDIS_URL`, `TELEGRAM_API_ID/HASH`, `TELEGRAM_SESSION_PATH` (`/data/telethon.session`), `TDL_CONFIG_DIR` (`/data/.tdl`), `TDL_OUTPUT_DIR_BASE` (`/data/tdl_output`), `LLM_API_KEY`, etc.
5.  `[ ]` Logging (`app/logging_config.py`).
6.  `[ ]` Database (`app/shared/db_models.py`, `app/shared/db_crud.py`):
    *   Define `MonitoredChat` SQLAlchemy model.
    *   Define `UserSettings` SQLAlchemy model (for per-user default prompt).
    *   Implement basic async CRUD functions for `MonitoredChat` (add, get, list, update, delete) and for `UserSettings` (set/get default prompt).
    *   SQLAlchemy async engine setup in `app/shared/db_models.py` or a `database.py`.
    *   **Supabase Setup:**  
        - If using SQL migrations, ensure `monitored_chats` and `user_settings` tables exist.
        - If using the Supabase dashboard, open the SQL editor and run [`app/shared/init_tables.sql`](app/shared/init_tables.sql) to create all required tables before starting the backend services.
        - You must do this step before running `init_db.py` or starting the bot for the first time.
7.  `[ ]` Redis Client & Queue (`app/shared/redis_client.py`).
8.  `[ ]` Telethon Client Helper (`app/userbot/client.py`).
9.  `[ ]` `tdl` Executor Stub (`app/worker/tdl_executor.py`): Define `async def execute_tdl_command(args: list[str], timeout_sec: int = 60) -> dict: raise NotImplementedError`.
10. `[ ]` Worker Task Stub (`app/worker/tasks.py`): `def process_monitored_chat(...): raise NotImplementedError`. `def periodic_monitoring_check(...): pass`.
11. `[ ]` Entry Points (`run_userbot.py`, `run_worker.py`, `run_scheduler.py`).
12. **[ ] `Dockerfile`:**
    *   Install Python, pip.
    *   **Install `tdl`:** Download appropriate prebuilt binary from `tdl` releases and place in `/usr/local/bin/` or similar. `chmod +x`.
    *   Install Python dependencies from `requirements.txt`.
    *   Copy application code.
13. **[ ] `fly.toml`:** Define `userbot`, `rqworker`, `rqscheduler` services. Define Redis app (or use external). Persistent volume `/data` mounted to ALL Python services. Map secrets. Set start commands.
14. **[ ] Initial Tests:** Config, Redis client, DB CRUD (mock DB session), basic `tdl_executor` (mock `subprocess`).
15. **[ ] Manual/Deployment Test:**
    *   Deploy to Fly.io. Create tables in Supabase (ensure `user_settings` table exists, see SQL above).
    *   `fly ssh console -s userbot` (or process group for userbot):
        *   Run `tdl login` *once* interactively. Ensure `TDL_CONFIG_DIR` is used.
        *   Run `run_userbot.py` *once* interactively for Telethon auth. Ensure `TELEGRAM_SESSION_PATH` is used.
    *   Verify all services start and connect (userbot to TG, all to Redis & Supabase). Check logs.

**End of Phase 1:** Deployable core infrastructure. `tdl` is available. Userbot authenticates. Workers and scheduler can start. DB is accessible.

---

## Phase 2: Userbot UI - Monitoring Management Commands

**Goal:** Implement Userbot Telethon handlers for `/monitor add/remove/list/prompt/run` commands, interacting with Supabase via CRUD functions.

**Steps (`app/userbot/handlers.py`, `app/userbot/ui.py`, `app/userbot/state.py` for temporary list caches if needed):**

1.  **[ ] CRUD for Monitoring (`app/shared/db_crud.py`):** Ensure all needed async CRUD functions for `MonitoredChat` are implemented and tested.
2.  **[ ] UI Helpers (`app/userbot/ui.py`):** `format_monitored_chats_list` for Telegram messages.
3.  **[ ] State Management (`app/userbot/state.py` - Optional for this Phase):** Only if `/monitor remove <number>` needs a temporary list cache in Redis. Otherwise, commands can be self-contained.
4.  **[ ] Event Handlers (`app/userbot/handlers.py`):**
    *   Use `async with async_sessionmaker() as db_session:` within handlers needing DB access.
    *   Implement `/monitor add`: Parses input, resolves `chat_identifier` via `client.get_entity`, calls `db_crud.add_monitored_chat`, responds.
    *   Implement `/monitor list`: Calls `db_crud.get_all_monitored_chats_for_user`, formats via `ui`, responds.
    *   Implement `/monitor remove`: Parses input, resolves, calls `db_crud.remove_monitored_chat`, responds.
    *   Implement `/monitor prompt`: Parses, resolves, calls `db_crud.update_monitored_chat_prompt`, responds.
    *   Implement `/monitor run`: Parses, resolves, gets `MonitoredChat` from DB. Enqueues `app.worker.tasks.process_monitored_chat` (see Phase 3). Responds "Manual run triggered...", stores status message ID in Redis via `state.store_status_message` (key like `status_msg:{request_id}`).
5.  **[ ] Register Handlers & Run Userbot (`run_userbot.py`).**
6.  **[ ] Testing:** Unit test handlers (mock Telethon, DB CRUD, RQ enqueue).
7.  **[ ] Manual Testing:** Deploy. Test all `/monitor` commands. Verify Supabase DB data.

**End of Phase 2:** User can manage monitored chat subscriptions via Telegram. Manual runs can be triggered (jobs enqueued but won't fully process yet).

---

## Phase 3: RQ Worker - `tdl` Orchestration, Cleaning, LLM

**Goal:** Implement the RQ worker task that uses `tdl_executor.py` to run `tdl` commands, parses JSON, cleans text, calls the LLM, and notifies progress/completion via Redis Pub/Sub. Implement the scheduled task.

**Steps:**

1.  **[ ] `tdl` Executor (`app/worker/tdl_executor.py`):**
    *   Implement `async def execute_tdl_command(args: list[str], timeout_sec: int = 300) -> dict:`
        *   Uses `asyncio.create_subprocess_exec('tdl', *args, stdout=PIPE, stderr=PIPE, env={... 'TDL_CONFIG_DIR': settings.TDL_CONFIG_DIR ...})`.
        *   `await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)`.
        *   Check `proc.returncode`. If non-zero, raise custom exception with stderr.
        *   Parse `stdout_data.decode()` as JSON. Handle `JSONDecodeError`.
        *   Return parsed JSON. Robust error logging.
2.  **[ ] LLM Service (`app/worker/llm_service.py`):** (As in v5.1, implement `get_llm_summary` with truncation).
3.  **[ ] Text Cleaner (`app/worker/text_cleaner.py`):** (Rename from `utils.py` if only for cleaning). Implement `clean_tdl_message_text` (takes a message object from `tdl` JSON).
4.  **[ ] Scheduled Task (`app/worker/tasks.py`):**
    *   Implement `periodic_monitoring_check(user_telegram_id: int):` Calls `db_crud.get_due_monitored_chats`, enqueues `process_monitored_chat` for each, updates `last_checked_at` in DB.
5.  **[ ] Main Worker Task (`app/worker/tasks.py`):**
    *   Implement `process_monitored_chat(monitored_chat_db_id: int, request_id: Optional[str] = None, is_manual_run: bool = False):`
        *   Job ID, Redis conn (for Pub/Sub), DB session. `publish_status` helper.
        *   Fetch `MonitoredChat` from DB.
        *   Define unique JSON output paths in `settings.TDL_OUTPUT_DIR_BASE` (e.g., using `request_id` or `job_id`).
        *   `publish_status('STARTED')`.
        *   **History:** `publish_status('TDL_HISTORY_EXPORT')`. Call `tdl_executor.execute_tdl_command(['chat', 'export', '-c', str(monitored_chat.chat_id), '--min-id', str(monitored_chat.last_processed_message_id), '--all', '-o', history_json_path])`.
        *   Parse history JSON. Clean messages using `text_cleaner`. Accumulate `cleaned_history_text`. Get `newest_message_id`.
        *   **Participants:** If group, `publish_status('TDL_PARTICIPANTS_EXPORT')`. Call `tdl_executor.execute_tdl_command(['chat', 'users', ...])`. Parse. Format `participants_text`.
        *   If no new history, `publish_status('NO_NEW_MESSAGES')`, update `last_processed_message_id` in DB, return success.
        *   `publish_status('CALLING_LLM')`. Call `llm_service.get_llm_summary`.
        *   Update `monitored_chat.last_processed_message_id` in DB.
        *   `publish_status('SUCCESS')`. Return dict.
        *   Handle all errors from `tdl_executor` and `llm_service`, `publish_status('FAILED', detail=...)`. Return failure dict.
6.  **[ ] `run_scheduler.py` (or `fly.toml` service):** Ensure it schedules `periodic_monitoring_check`.
7.  **[ ] Testing:** Unit test `tdl_executor` (mock `asyncio.create_subprocess_exec`). Unit test `llm_service`. Unit test `tasks.process_monitored_chat` (mock `tdl_executor`, `llm_service`, DB CRUD, Redis publish).
8.  **[ ] Manual Testing:** Trigger jobs (manual/scheduled). Check worker logs. Check `tdl_output` files. Check Pub/Sub. Check DB updates.

**End of Phase 3:** Automated pipeline using `tdl` for extraction, cleaning, LLM processing, and status publishing.

---

## Phase 4: Userbot - Handling Pub/Sub Events & Delivering Insights

**Goal:** Userbot listens to Redis Pub/Sub, updates Telegram status messages (for manual runs), and sends LLM insights/participant files to the user.

**Steps (`app/userbot/event_listener.py`, `app/userbot/ui.py`, `app/userbot/results_sender.py`):**

1.  **[ ] Pub/Sub Listener (`app/userbot/event_listener.py`):**
    *   Implement `async def listen_for_job_events(client, settings):` Subscribes to `request_status:*`.
    *   On message: Parse JSON. Get `request_id` (or other context to find `status_message_id` for manual runs).
    *   If status is `PROGRESS` or intermediate from worker, call `ui.update_manual_run_status_message`.
    *   If status `SUCCESS` or `FAILED` (final from worker's return dict published): Call `handle_insight_job_completion`.
2.  **[ ] Job Completion Handler (`event_listener.py`):**
    *   Implement `async def handle_insight_job_completion(client, job_id_or_request_id, settings):`
        *   Fetch final job result/details from where worker stored it (e.g., if worker task returns a dict, RQ stores it; or worker task can write to a specific Redis key `result:{job_id}`).
        *   Get `user_id`, `chat_id`, `chat_title`, `summary`, `participants_file_path`, `error`, `status_message_id_for_manual_run`.
        *   If success: Call `results_sender.send_llm_insight_and_files`. Update manual run status message.
        *   If failure: Call `results_sender.send_failure_insight_message`. Update manual run status message.
3.  **[ ] Results Sender (`app/userbot/results_sender.py`):**
    *   Implement `async def send_llm_insight_and_files(client, user_id, chat_title, summary, participants_file_path):`
        *   Send summary message. Handle length.
        *   If `participants_file_path` exists, `client.send_file`, then `os.remove` from persistent disk.
    *   Implement `async def send_failure_insight_message(client, user_id, chat_title, error_message):`
4.  **[ ] UI Update (`app/userbot/ui.py`):** Implement `async def update_manual_run_status_message(...)`.
5.  **[ ] Start Listener (`run_userbot.py`).**
6.  **[ ] Testing:** Unit test event listener logic, completion handler, results sender.
7.  **[ ] Manual Testing:** Full end-to-end. Check Telegram for insight messages and files. Check status edits for manual runs.

**End of Phase 4:** Complete, polished user experience within Telegram.

---

## Phase 5: Polishing, Advanced Features & Productionizing

**Goal:** Refine UX, add features like `/settings`, ensure stability on Fly.io.

**Steps:**

1.  **[ ] `/settings` Command:** Allow user to set default LLM prompt or per-chat preferences via inline keyboards, store in Supabase.
2.  **[ ] Enhanced `/status` Command:** Userbot command to query Supabase for status of recent/ongoing monitored chat processing.
3.  **[ ] `/pause` & `/resume` Monitoring:** Toggle `is_active` in `MonitoredChat` table.
4.  **[ ] `/cancel` RQ Jobs (Advanced):** For manual runs, allow cancellation. RQ jobs can be cancelled. Update status message.
5.  **[ ] Robust Error Handling:** More specific error messages to user. Better logging of `tdl` stderr.
6.  **[ ] Fly.io Config:** Optimize `fly.toml` (resources, scaling for `rqworker`, health checks).
7.  **[ ] File Cleanup:** Robust cleanup for `tdl_output` intermediate JSONs and any orphaned TXT files on the persistent volume.
8.  **[ ] README:** Finalize with Fly.io deployment, Supabase setup, initial `tdl login` & Telethon auth via `fly ssh console`, all user commands.
9.  **[ ] Security Review:** Secrets, file paths, `tdl` execution environment.
10. **[ ] Load Testing (Conceptual):** Monitor performance if user monitors many very active chats.

**End of Phase 5:** A highly refined, feature-rich, and robust personal Telegram insight agent.