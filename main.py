import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # e.g., https://your-bot-name.onrender.com

app = Flask(__name__)

# --- AI REPLY FUNCTION ---
def get_ai_response(prompt):
    try:
        url = "https://api.monkedev.com/fun/chat"
        params = {"msg": prompt, "uid": "kioto_ai"}
        res = requests.get(url, params=params)
        data = res.json()
        return data.get("response", "Hmm... I didn’t get that, try again?")
    except Exception:
        return "Sorry, my brain lagged out 💀"

# --- TELEGRAM HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! I’m your AI friend 🤖. Tell me anything — I’ll listen and talk with you!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply)

# --- BUILD THE APP ---
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

@app.route("/")
def home():
    return "Bot is alive ✅"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# --- RUN WEBHOOK ---
async def set_webhook():
    webhook_url = f"{APP_URL}/{BOT_TOKEN}"
    await application.bot.set_webhook(url=webhook_url)
    print(f"Webhook set to {webhook_url}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

