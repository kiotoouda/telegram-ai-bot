import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Example: https://telegram-ai-bot-xxxxx.onrender.com

# Flask server for webhook
server = Flask(__name__)

# AI function
def get_ai_response(prompt):
    try:
        url = "https://api.monkedev.com/fun/chat"
        params = {"msg": prompt, "uid": "kioto_ai"}
        res = requests.get(url, params=params)
        data = res.json()
        return data.get("response", "Hmm... I didn’t get that, try again?")
    except Exception:
        return "Sorry, my brain lagged out 💀"


# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! I’m alive on Render via webhook ⚡️")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply)


# Telegram app setup
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))


# Webhook endpoint
@server.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200


@server.route('/')
def index():
    return "Bot is running on webhook mode.", 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=BOT_TOKEN,
        webhook_url=f"{APP_URL}/{BOT_TOKEN}"
    )
    server.run(host="0.0.0.0", port=port)
