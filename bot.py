import os
from pyrogram import Client, filters

# Render ke environment variables se API details lenge
api_id = int(os.environ.get("31545473", 0))
api_hash = os.environ.get("20e6f4ba06ca479f23a8b8b606888bc5", "")

# Client start hoga jo personal ID se message bheja karega
app = Client("my_account_session", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.private & filters.command("start"))
def send_welcome(client, message):
    # Yeh raha naya welcome message jo personal ID se jayega
    welcome_text = "Hi dear , admin of JetQueen silpa Aviator here for you ❤️‍🔥\n\nAap aviator aur 1win khelte ho ❓❓❓"
    message.reply_text(welcome_text)

print("Userbot script ready ho rahi hai...")
app.run()
