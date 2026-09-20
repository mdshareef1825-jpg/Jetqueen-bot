import asyncio
import os
from pyrogram import Client

# Render ke environment variables se session string uthayega
SESSION_STRING = os.environ.get("SESSION")

# Client initialize kar rahe hain
app = Client(
    "silpa_bot",
    session_string=SESSION_STRING
)

async def main():
    async with app:
        print("Bot successfully start ho gaya hai!")
        # Silpa ke messages aur join requests handle karne ke liye bot active rahega
        await asyncio.idle()

if name == "__main__":
    asyncio.run(main())
