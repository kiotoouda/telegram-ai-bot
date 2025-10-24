import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Set this in Render: https://your-render-url.com

app = Flask(__name__)

# Create bot application
app.bot_app = Application.builder().token(BOT_TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is alive and ready!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app.bot_app.add_handler(CommandHandler("start", start))
app.bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook route
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot_app.bot)
    asyncio.get_event_loop().create_task(app.bot_app.update_queue.put(update))
    return "OK", 200

if __name__ == "__main__":
    # Set webhook on startup
    async def set_webhook():
        await app.bot_app.bot.set_webhook(f"{APP_URL}/{BOT_TOKEN}")
    asyncio.get_event_loop().run_until_complete(set_webhook())
    
    # Run Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
