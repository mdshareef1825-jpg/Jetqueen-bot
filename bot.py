Zeeshan:
import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, CommandHandler, MessageHandler, filters, ContextTypes

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

# YAHAN APNA TELEGRAM USER ID DALNA HAI (00000000 ki jagah apna number likhein)
ADMIN_USER_ID = 8330567363  

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
    "📩 After deposit, send your ID or Screenshot here — I’ll add you to VIP Group FREE 🔥"
)

KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🚀 Create 1WIN ID Now", url="https://lkfg.pro/83ee896d")]
])

# 1. Handle Channel Join Requests
async def auto_approve_and_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    chat = request.chat

    try:
        await context.bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
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

# 2. Handle /start command
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

# 3. Handle User Messages & Admin Replies (The Magic Bridge)
async def handle_message_forwarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.from_user:
        return

    user_id = message.from_user.id

    # CASE A: Agar message Admin ki taraf se aaya hai aur kisi message par Reply kiya gaya hai
    if user_id == ADMIN_USER_ID and message.reply_to_message:
        replied_msg = message.reply_to_message
        
        target_user_id = None
        if "user_id_map" in context.bot_data and replied_msg.message_id in context.bot_data["user_id_map"]:
            target_user_id = context.bot_data["user_id_map"][replied_msg.message_id]

        if target_user_id:
            try:
                await context.bot.copy_message(
                    chat_id=target_user_id,
                    from_chat_id=message.chat_id,
                    message_id=message.message_id
                )
                await message.reply_text("✅ Reply sent to user!")
            except Exception as e:
                await message.reply_text(f"❌ Failed to send: {e}")
        else:
            await message.reply_text("❌ Error: Target user not found for this message.")
        return

    # CASE B: Agar message kisi aam User (Customer) ki taraf se aaya hai
    if user_id != ADMIN_USER_ID:
        try:
            forwarded = await context.bot.forward_message(
                chat_id=ADMIN_USER_ID,

from_chat_id=message.chat_id,
                message_id=message.message_id
            )
            
            user_info = f"👤 From: {message.from_user.first_name} (ID: `{user_id}`)"
            sent_info = await context.bot.send_message(
                chat_id=ADMIN_USER_ID,
                text=user_info,
                parse_mode="Markdown"
            )

            if "user_id_map" not in context.bot_data:
                context.bot_data["user_id_map"] = {}
            
            context.bot_data["user_id_map"][sent_info.message_id] = user_id

        except Exception as e:
            print(f"Error forwarding message: {e}")

if name == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()

    if not TOKEN:
        print("ERROR: BOT_TOKEN is missing in Environment Variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Register Handlers
        app.add_handler(ChatJoinRequestHandler(auto_approve_and_welcome))
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message_forwarding))
        
        print("Bot is starting with Forwarding System...")
        app.run_polling(stop_signals=None)
