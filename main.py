import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# -------------------------------
# Environment variables
# -------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Set this in Render Environment
APP_URL = os.environ.get("APP_URL")      # Set this to your Render URL

# -------------------------------
# Initialize Flask
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Bot Handlers
# -------------------------------
async def start(update: Update, context):
    await update.message.reply_text("Hello! I am your AI Telegram bot 🤖")

async def echo(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

# -------------------------------
# Initialize Telegram Bot
# -------------------------------
bot_app = Application.builder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Store main event loop
bot_app.loop = asyncio.get_event_loop()

# -------------------------------
# Webhook route
# -------------------------------
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    # Run in the bot's event loop safely
    asyncio.run_coroutine_threadsafe(bot_app.update_queue.put(update), bot_app.loop)
    return "OK", 200

# -------------------------------
# Main entrypoint
# -------------------------------
if __name__ == "__main__":
    # Set webhook with Telegram API
    import requests
    webhook_url = f"{APP_URL}/{BOT_TOKEN}"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")
    
    # Start Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
