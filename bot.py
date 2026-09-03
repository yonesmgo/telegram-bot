
import os
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

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text

    if not text:
        return

    # پاسخ به سلام
    if text.strip() == "سلام":
        await update.message.reply_text("سلام 🌹 خوش آمدید")


# =========================
# Webhook
# =========================

application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)


@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    await application.initialize()
    await application.process_update(update)
    await application.shutdown()

    return "OK"


# =========================
# Run Flask
# =========================

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    Thread(target=run).start()

