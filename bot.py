import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def auto_approve_and_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    chat = request.chat

    try:
        # 1. Automatically approve the join request
        await context.bot.approve_chat_join_request(
            chat_id=chat.id,
            user_id=user.id
        )
        print(f"Approved {user.first_name} in {chat.title}")

        # 2. Formatted welcome message
        welcome_text = (
            "Welcome To The Jetqueen Silpa Aviator Channel 🔥\n\n"
            "Ready to earn with 1WIN Aviator? 💸\n"
            "Follow these 3 quick steps 👇\n\n"
            "1️⃣ Create ID: [https://lkfg.pro/83ee896d](https://lkfg.pro/83ee896d)\n\n"
            "2️⃣ Use Promo Code: **DS745**\n"
            "3️⃣ Deposit ₹500+ for India or 10 dollar for others to get prime + bot token\n\n"
            "✅ VIP Signals\n"
            "✅ Prime Channel Access\n"
            "✅ Personal Loss Recovery Sessions\n"
            "✅ Super-Fast Withdrawal 🚀\n\n"
            "📩 After deposit, send your ID — I’ll add you to VIP Group FREE 🔥"
        )

        # 3. Direct registration button
        keyboard = [[InlineKeyboardButton("🚀 Create 1WIN ID Now", url="https://lkfg.pro/83ee896d")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # 4. Send private message to user
        await context.bot.send_message(
            chat_id=user.id,
            text=welcome_text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error handling request: {e}")

if name == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(auto_approve_and_welcome))
    print("Bot is starting...")
    app.run_polling()
