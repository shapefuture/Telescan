# Telegram Userbot Extractor – Setup Instructions

## Database Setup (Supabase/Postgres)

**Required tables:**  
- `monitored_chats`  
- `user_settings`

Before running the backend services for the first time, you must ensure the required tables exist in your Supabase/Postgres instance.

**Option 1: Manual (Supabase Dashboard)**  
1. Open the Supabase dashboard for your project.
2. Go to the SQL Editor.
3. Copy and run the contents of [`app/shared/init_tables.sql`](app/shared/init_tables.sql).

**Option 2: Automated (Python Script)**  
If you have direct Postgres access (not just Supabase), you can run:
```bash
python app/shared/init_db.py
```
This will create all tables defined in the ORM.

**IMPORTANT:**  
Do this before starting the userbot, worker, or scheduler services.

---
