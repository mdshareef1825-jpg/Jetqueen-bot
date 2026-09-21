import sys
import asyncio

# Python 3.14 event loop compatibility fix
if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        try:
            loop = asyncio.get_event_loop_policy().get_event_loop()
        except Exception:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, Message

API_ID = 31545473
API_HASH = "20e6f4ba06ca479f23a8b8b606888bc5"
SESSION_STRING = "BQHhWIEApyEut3QSUgybCvDehu-5UbMAXN2PkptDiVgeW_eRM0DYvHClkLb5Mf8mGvXieK4KevG5gn2_MDngl4sBD0Q-ZpEZUyUo7T_qU1kyg22eYfT7dwRdj1pNTPR9c8ZxMMtdCouVCGXjBrVN9JY_5G7tJU-sr0rSO5D8tEhC78Rql1ktvt6kcR2rQaR0f-7lsqhBtRgWu2ePq4BXWc2TVVLEQCdC1SIsj_UyPFbWIkQwq03oMPSMgZQPmnVVz5PMchAj0_GQ5NOF3hGH9QvN9hqYmGEyLWVI3Xos0X7kvTLMYVLHQKSNbiZ3OiTPSWxOwCk0VrSG9Veqv0C2U4ztr5PSqwAAAAITrWxxAA"

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Track kiya hua set taaki ek user ko baar-baar welcome message na jaye
welcomed_users = set()

# 1. Jab koi Join Request bhejega toh auto-accept karke welcome message jayega
@app.on_chat_join_request()
async def accept_join_request(client, request: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        print(f"Join request accepted for: {request.from_user.first_name}")
        
        user_id = request.from_user.id
        if user_id not in welcomed_users:
            welcome_text = "Hi! Welcome. Silpa this side, further conversation hum yahan continue kar sakte hain."
            await client.send_message(user_id, welcome_text)
            welcomed_users.add(user_id)
            print(f"Sent welcome message to {request.from_user.first_name}")
            
    except Exception as e:
        print(f"Error in join request handler: {e}")

# 2. Jab koi direct group join karega toh bhi welcome message chala jayega
@app.on_message(filters.group & filters.new_chat_members)
async def direct_join_welcome(client, message: Message):
    try:
        for new_user in message.new_chat_members:
            # Agar bot khud add hua hai toh ignore karo
            if new_user.id == (await client.get_me()).id:
                continue
                
            user_id = new_user.id
            if user_id not in welcomed_users:
                welcome_text = "Hi! Welcome. Silpa this side, further conversation hum yahan continue kar sakte hain."
                await client.send_message(user_id, welcome_text)
                welcomed_users.add(user_id)
                print(f"Sent direct join welcome message to {new_user.first_name}")
    except Exception as e:
        print(f"Error in direct join handler: {e}")

if __name__ == "__main__":
    print("Userbot is starting with precise welcome & join handlers...")
    app.run()
