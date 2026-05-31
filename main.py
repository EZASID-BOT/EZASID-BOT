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
