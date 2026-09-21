import asyncio
import sys
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest

API_ID = 31545473  # Apni API ID dalein
API_HASH = "20e6f4ba06ca479f23a8b8b606888bc5"  # Apna API Hash dalein
SESSION_STRING = "BQHhWIEApyEut3QSUgybCvDehu-5UbMAXN2PkptDiVgeW_eRM0DYvHClkLb5Mf8mGvXieK4KevG5gn2_MDngl4sBD0Q-ZpEZUyUo7T_qU1kyg22eYfT7dwRdj1pNTPR9c8ZxMMtdCouVCGXjBrVN9JY_5G7tJU-sr0rSO5D8tEhC78Rql1ktvt6kcR2rQaR0f-7lsqhBtRgWu2ePq4BXWc2TVVLEQCdC1SIsj_UyPFbWIkQwq03oMPSMgZQPmnVVz5PMchAj0_GQ5NOF3hGH9QvN9hqYmGEyLWVI3Xos0X7kvTLMYVLHQKSNbiZ3OiTPSWxOwCk0VrSG9Veqv0C2U4ztr5PSqwAAAAITrWxxAA"  # Apni Session String dalein

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.on_chat_join_request()
async def accept_join_request(client, request: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        print(f"Join request accepted for: {request.from_user.first_name}")
    except Exception as e:
        print(f"Error accepting request: {e}")

@app.on_message(filters.private & ~filters.me)
async def welcome_message(client, message):
    try:
        welcome_text = "Hi! Welcome. Silpa this side, further conversation hum yahan continue kar sakte hain."
        await client.send_message(message.chat.id, welcome_text)
        print(f"Sent welcome message to {message.from_user.first_name}")
    except Exception as e:
        print(f"Error sending message: {e}")

async def main():
    print("Userbot is starting...")
    await app.start()
    await asyncio.Event().wait()

if name == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())
