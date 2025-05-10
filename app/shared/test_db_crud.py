# Minimal async test for CRUD operations

import asyncio
from app.shared.database import async_sessionmaker
from app.shared import db_crud

TEST_USER_ID = 123456789
TEST_CHAT_ID = -100987654321
TEST_TITLE = "Test Chat"
TEST_PROMPT = "Summarize everything"
NEW_PROMPT = "Summarize only important messages"

async def main():
    async with async_sessionmaker() as session:
        # Add
        mc = await db_crud.add_monitored_chat(
            session=session,
            user_id=TEST_USER_ID,
            chat_id=TEST_CHAT_ID,
            chat_title=TEST_TITLE,
            prompt=TEST_PROMPT,
        )
        print("Added:", mc.id, mc.chat_title)

        # Get
        mc2 = await db_crud.get_monitored_chat(session, TEST_USER_ID, TEST_CHAT_ID)
        print("Fetched:", mc2.id, mc2.prompt)

        # Update
        rows = await db_crud.update_monitored_chat_prompt(session, TEST_USER_ID, TEST_CHAT_ID, NEW_PROMPT)
        print("Prompt updated:", rows)

        # List
        all_chats = await db_crud.get_all_monitored_chats_for_user(session, TEST_USER_ID)
        print("Chats for user:", [c.chat_title for c in all_chats])

        # Remove
        removed = await db_crud.remove_monitored_chat(session, TEST_USER_ID, TEST_CHAT_ID)
        print("Removed:", removed)

if __name__ == "__main__":
    asyncio.run(main())