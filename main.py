import os
import telebot
from google import genai

# ከ Render Environment የሚወስድበት መንገድ
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

# ቦቱን እና የጀሚኒ ክላይንትን ማዋቀር
bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=API_KEY)

# የጀሚኒ ሞዴልን መጠቀም (ለምሳሌ gemini-2.0-flash)
def get_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"ስህተት ተፈጥሯል: {str(e)}"

# የቴሌግራም መልእክት ሲመጣ
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    reply = get_ai_response(user_text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    print("ቦቱ እየሰራ ነው...")
    bot.polling()
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render የሚሰጠውን PORT ይጠቀማል፣ ካልተገኘ 8080 ይጠቀማል
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ይህንን በፋይልህ መጨረሻ ላይ አስቀምጠው
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    # ከዚህ በታች ቦትህን የሚያስጀምረው ኮድህ ይቀጥላል (ለምሳሌ bot.run())
from telegram import BotCommand

async def set_commands(bot):
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

# ይህንን በ main() ውስጥ ወይም ቦቱ በሚነሳበት ቦታ ላይ ይጠሩታል:
# await set_commands(bot)

