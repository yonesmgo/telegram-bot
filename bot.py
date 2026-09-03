import os
import asyncio
from threading import Thread

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# =========================
# Flask Server
# =========================

app = Flask(__name__)


@app.route("/")
def home():
    return "Telegram Bot is running!"


# =========================
# Telegram Bot
# =========================

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
ALLOWED_GROUP_ID = -1001895986483

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL environment variable is not set")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    # فقط همین گروه مجاز است
    if not update.effective_chat:
        return

    if update.effective_chat.id != ALLOWED_GROUP_ID:
        return

    text = update.message.text

    if not text:
        return

    if text.strip() == "سلام":
        await update.message.reply_text("سلام 🌹 خوش آمدید")


application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)


# =========================
# Telegram Event Loop
# =========================

telegram_loop = asyncio.new_event_loop()


def start_telegram():
    asyncio.set_event_loop(telegram_loop)
    telegram_loop.run_until_complete(application.initialize())
    telegram_loop.run_until_complete(
        application.bot.set_webhook(url=WEBHOOK_URL)
    )
    print(f"Telegram webhook set to: {WEBHOOK_URL}")
    telegram_loop.run_forever()


telegram_thread = Thread(target=start_telegram, daemon=True)
telegram_thread.start()


# =========================
# Webhook Endpoint
# =========================

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, application.bot)

    future = asyncio.run_coroutine_threadsafe(
        application.process_update(update),
        telegram_loop
    )

    future.result(timeout=20)

    return "OK"


# =========================
# Run Flask
# =========================

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    run()
