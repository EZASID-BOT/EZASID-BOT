import os
import logging
import asyncio
from flask import Flask
from threading import Thread
from telegram import Bot, BotCommand, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# --- Configuration ---
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# --- Setup Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Gemini AI Configuration ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Flask Web Server (ለ Render) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot Commands ---
async def set_commands(bot: Bot):
    commands = [
        BotCommand("menu", "Show the main menu"),
        BotCommand("upload", "Upload an Ethiopian ID PDF"),
        BotCommand("topup", "Buy a credit package"),
        BotCommand("balance", "Check your credit balance"),
        BotCommand("jobs", "Recent ID jobs"),
        BotCommand("dashboard", "Open the web dashboard"),
        BotCommand("profile", "Your profile"),
        BotCommand("settings", "Output settings"),
        BotCommand("language", "Change language"),
        BotCommand("refer", "Your referral link"),
        BotCommand("help", "Help"),
        BotCommand("cancel", "Cancel the current flow"),
    ]
    await bot.set_my_commands(commands)

# --- Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # Flask ሰርቨርን ይጀምራል
    Thread(target=run_flask).start()

    # ቦቱን ይጀምራል
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Commands አዘጋጅ
    asyncio.run(set_commands(application.bot))
    
    # Message Handler አክል
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is starting...")
    application.run_polling()
