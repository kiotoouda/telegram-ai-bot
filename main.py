import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")

app = Flask(__name__)

# -------------------------------
# Handlers
# -------------------------------
async def start(update: Update, context):
    await update.message.reply_text("Hello! I am your AI Telegram bot 🤖")

async def echo(update: Update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

# -------------------------------
# Initialize Bot
# -------------------------------
bot_app = Application.builder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# -------------------------------
# Webhook route
# -------------------------------
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)

    # Use asyncio.run() for each request (creates temporary loop)
    asyncio.run(bot_app.update_queue.put(update))

    return "OK", 200

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    import requests

    # Set webhook
    webhook_url = f"{APP_URL}/{BOT_TOKEN}"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")

    # Start Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


