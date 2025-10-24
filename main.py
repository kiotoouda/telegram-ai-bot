import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# -------------------------------
# Environment variables
# -------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Set in Render Environment

# -------------------------------
# Bot Handlers
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI Telegram bot 🤖")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

# -------------------------------
# Initialize Telegram Bot
# -------------------------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot started... Polling now.")
    app.run_polling()  # <-- This will keep the bot alive

if __name__ == "__main__":
    main()
