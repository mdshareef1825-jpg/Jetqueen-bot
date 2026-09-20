import os
from pyrogram import Client

# Render ke environment variables se session string uthayega
SESSION_STRING = os.environ.get("SESSION")

# Client initialize karein
app = Client(
    "silpa_bot",
    session_string=SESSION_STRING
)

# Pyrogram ka built-in .run() method sabse safe hai aur event loop khud sambhal leta hai
if name == "__main__":
    app.run()
