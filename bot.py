import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, CommandHandler, ContextTypes

# Health check server for Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

TOKEN = os.environ.get("BOT_TOKEN", "").strip()

logging.basicConfig(level=logging.INFO)

# Welcome Promo Message & Button
WELCOME_TEXT = (
    "Welcome To The Jetqueen Silpa Aviator Channel 🔥\n\n"
    "Ready to earn with 1WIN Aviator? 💸\n"
    "Follow these 3 quick steps 👇\n\n"
    "1️⃣ Create ID: https://lkfg.pro/83ee896d\n\n"
    "2️⃣ Use Promo Code: **DS745**\n"
    "3️⃣ Deposit ₹500+ for India or 10 dollar for others to get prime + bot token\n\n"
    "✅ VIP Signals\n"
    "✅ Prime Channel Access\n"
    "✅ Personal Loss Recovery Sessions\n"
    "✅ Super-Fast Withdrawal 🚀\n\n"
    "📩 After deposit, send your ID — I’ll add you to VIP Group FREE 🔥"
)

KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🚀 Create 1WIN ID Now", url="https://lkfg.pro/83ee896d")]
])

# 1. Handle Join Requests (Auto-approve & send DM if possible)
async def auto_approve_and_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    chat = request.chat

    try:
        await context.bot.approve_chat_join_request(
            chat_id=chat.id,
            user_id=user.id
        )
        print(f"Approved {user.first_name} in {chat.title}")

        await context.bot.send_message(
            chat_id=user.id,
            text=WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=KEYBOARD,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error handling join request: {e}")

# 2. Handle /start command (Instant reply when user taps Start)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            text=WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=KEYBOARD,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error handling start command: {e}")

if name == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()

    if not TOKEN:
        print("ERROR: BOT_TOKEN is missing in Environment Variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Register both handlers
        app.add_handler(ChatJoinRequestHandler(auto_approve_and_welcome))
        app.add_handler(CommandHandler("start", start_command))
        
        print("Bot is starting...")
        app.run_polling(stop_signals=None)
