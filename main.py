import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Free AI API (no key needed)
def get_ai_response(prompt):
    try:
        res = requests.get(f"https://api.affiliateplus.xyz/api/chatbot?message={prompt}&botname=AI%20Friend&ownername=Kioto")
        return res.json().get("message", "Hmm, I didn't get that. Can you repeat?")
    except Exception as e:
        return "Sorry, my brain lagged out 💀"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! I’m your AI friend 🤖. Tell me anything — I’ll listen and talk with you!")

# When user sends a message
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply)

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
