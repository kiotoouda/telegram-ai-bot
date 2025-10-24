import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

async def start(update: Update, context):
    await update.message.reply_text("Hello! I am your AI Telegram bot 🤖")

async def echo(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

bot_app = Application.builder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.run_coroutine_threadsafe(bot_app.update_queue.put(update), bot_app.loop)
    return "OK", 200

if __name__ == "__main__":
    import requests
    webhook_url = f"{APP_URL}/{BOT_TOKEN}"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")

    # Start the bot's internal loop without polling
    bot_app.initialize()  # Initializes the event loop
    app.run(host="0.0.0.0", port=PORT)
