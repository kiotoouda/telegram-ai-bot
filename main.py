import os
import asyncio
import threading
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# -------------------------------
# Environment variables
# -------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Render Environment
APP_URL = os.environ.get("APP_URL")      # Render Environment

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

# Start the bot loop in a background thread
def start_bot():
    bot_app.initialize()  # Initialize internal queues
    bot_app.start()       # Start processing updates

threading.Thread(target=start_bot, daemon=True).start()

# -------------------------------
# Webhook route
# -------------------------------
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    loop = asyncio.get_event_loop()
    # Put update into bot queue safely
    asyncio.run_coroutine_threadsafe(bot_app.update_queue.put(update), loop)
    return "OK", 200

# -------------------------------
# Main entrypoint
# -------------------------------
if __name__ == "__main__":
    # Set webhook with Telegram API
    webhook_url = f"{APP_URL}/{BOT_TOKEN}"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")
    
    # Start Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
