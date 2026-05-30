import os
import telebot
from telebot import types
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
import google.generativeai as genai

# --- የቁልፎች ማገናኛ (የላክሃቸው መረጃዎች) ---
BOT_TOKEN = "8673924309:AAGXgULwObYVubreWcDUVGLtww3DXN2TN10"
GEMINI_API_KEY = "AQ.Ab8RN6Js3KRUi-P0n9nw0dtdj7pttFVQq7yQIVaQEFx-7T1Wdw"

# ቦቶቹን የማንቂያ ሲስተም
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# የ Gemini AI ሞዴል ማዋቀሪያ
ai_model = genai.GenerativeModel('gemini-pro')

# መደበኛ የ ID Card መጠን በፒክስል (300 DPI ለላቀ ጥራት)
ID_WIDTH = 1011
ID_HEIGHT = 638

def enhance_and_resize_image(image_path, output_path):
    """የፎቶውን ጥራት እጅግ በጣም አሳምሮ ወደ ID መጠን ይቀይራል"""
    with Image.open(image_path) as img:
        # 1. መጀመሪያ ፎቶውን ወደ ID Card መጠን መቀየር
        resized_img = img.resize((ID_WIDTH, ID_HEIGHT), Image.Resampling.LANCZOS)
        
        # 2. የፎቶውን ጥራት ማሳመሪያ (Enhancement)
        # ቀለም ማድመቅ
        color_enhancer = ImageEnhance.Color(resized_img)
        resized_img = color_enhancer.enhance(1.15)
        
        # ጽሁፎች በደንብ እንዲያነቡ ሹልነት (Sharpness) መጨመር
        sharpness_enhancer = ImageEnhance.Sharpness(resized_img)
        resized_img = sharpness_enhancer.enhance(1.4)
        
        # የብርሃን ንፅፅር ማስተካከል
        contrast_enhancer = ImageEnhance.Contrast(resized_img)
        resized_img = contrast_enhancer.enhance(1.05)

        # 3. በ 300 DPI ከፍተኛ ጥራት ሴቭ ማድረግ
        resized_img.save(output_path, "PNG", dpi=(300, 300), quality=100)

def get_main_keyboard():
    """ለቢዝነስ የሚሆኑ ዋና ዋና በተኖች"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_balance = types.KeyboardButton("💰 Balance")
    btn_deposit = types.KeyboardButton("💳 Deposit")
    btn_legal = types.KeyboardButton("⚖️ Legal Research")
    btn_scan = types.KeyboardButton("📄 Document Scan")
    btn_help = types.KeyboardButton("ℹ️ Help")
    btn_admin = types.KeyboardButton("🛠 Admin Panel")
    
    markup.add(btn_balance, btn_deposit)
    markup.add(btn_legal, btn_scan)
    markup.add(btn_help, btn_admin)
    return markup

# --- የቦት ትዕዛዞች መስሪያ ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 እንኳን ወደ አዲሱ የቢዝነስ ቦትዎ በደህና መጡ!\n\n"
        "✨ **ዋና አገልግሎታችን፡** የኢትዮጵያን ብሔራዊ መታወቂያ (National ID) "
        "ከ PDF ወይም ከስክሪንሾት ወደ ትክክለኛ የካርድ መጠን (8.56 cm x 5.4 cm) በከፍተኛ ጥራት መቀየር ነው።\n\n"
        "🤖 በተጨማሪም ማናቸውንም የንግድ ወይም አጠቃላይ ጥያቄዎች እዚህ ቢጽፉልኝ በ AI የታገዘ ምላሽ እሰጥዎታለሁ።\n\n"
        "👇 ለመጀመር ከታች ያሉትን በተኖች ይጠቀሙ።"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# 'Document Scan' በተን ሲጫኑ
@bot.message_handler(func=lambda message: message.text == "📄 Document Scan")
def ask_for_document(message):
    bot.send_message(message.chat.id, "📸 እባክዎ የ National ID ፎቶ (Screenshot) ወይም PDF ፋይል ይላኩልኝ። በከፍተኛ ጥራት አስተካክዬ እመልስልዎታለሁ።")

# ዶክመንት (PDF ወይም ፋይል) ሲላክ
@bot.message_handler(content_types=['document'])
def handle_document_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        file_name = message.document.file_name
        input_path = f"in_{file_name}"
        output_path = "enhanced_id_card.png"
        
        with open(input_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        bot.reply_to(message, "⏳ ፎቶውን እያሳመርኩና መጠኑን ወደ ID ካርድ እየቀየርኩ ነው፣ እባክዎ ጥቂት ሰከንዶች ይጠብቁ...")

        if file_name.lower().endswith('.pdf'):
            pages = convert_from_path(input_path, dpi=300)
            if pages:
                pages[0].save("pdf_temp.png", "PNG")
                enhance_and_resize_image("pdf_temp.png", output_path)
                os.remove("pdf_temp.png")
            else:
                raise Exception("PDF ፋይሉን ማንበብ አልተቻለም።")
        else:
            enhance_and_resize_image(input_path, output_path)

        with open(output_path, 'rb') as final_id:
            bot.send_document(
                message.chat.id, 
                final_id, 
                caption="✅ የእርስዎ National ID በጥራት ታድሶ በተስተካከለ መጠን (8.56 cm x 5.4 cm) ተዘጋጅቷል!",
                reply_markup=get_main_keyboard()
            )
            
        os.remove(input_path)
        os.remove(output_path)

    except Exception as e:
        bot.reply_to(message, f"❌ ስህተት አጋጥሟል፦ {str(e)}")

# ቀጥታ ፎቶ (Screenshot) ሲላክ
@bot.message_handler(content_types=['photo'])
def handle_photo_image(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        input_path = "in_screenshot.png"
        output_path = "enhanced_id_card.png"
        
        with open(input_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        bot.reply_to(message, "⏳ የስክሪንሾቱን ጥራት በመጨመርና መጠን በመቀየር ላይ ነኝ...")
        
        enhance_and_resize_image(input_path, output_path)
        
        with open(output_path, 'rb') as final_id:
            bot.send_document(
                message.chat.id, 
                final_id, 
                caption="✅ ስክሪንሾቱ ወደ ID ካርድ መጠን ተቀይሮ ጥራቱ እንዲያምር ተደርጓል!",
                reply_markup=get_main_keyboard()
            )
            
        os.remove(input_path)
        os.remove(output_path)

    except Exception as e:
        bot.reply_to(message, f"❌ ስህተት አጋጥሟል፦ {str(e)}")

# --- ለቢዝነስ በተኖች እና ለ Gemini AI ምላሽ መስጫ ክፍል ---
@bot.message_handler(func=lambda message: True)
def handle_text_and_buttons(message):
    user_text = message.text

    if user_text == "💰 Balance":
        bot.reply_to(message, "💵 የአሁኑ ቀሪ ሂሳብዎ 0.00 ብር ነው።")
    elif user_text == "💳 Deposit":
        bot.reply_to(message, "🏦 ሂሳብ ለመሙላት እባክዎ የቴሌብር ወይም የባንክ አካውንታችንን ይጠቀሙ።")
    elif user_text == "⚖️ Legal Research":
        bot.reply_to(message, "📂 ወደ ህግ ምርምር ክፍል እንኳን በደህና መጡ። እባክዎ የሚፈልጉትን የህግ ጉዳይ ወይም የሰነድ ሀሳብ እዚህ ይጻፉልኝ፤ በ AI ፈልጌ እሰጥዎታለሁ።")
    elif user_text == "ℹ️ Help":
        bot.reply_to(message, "💡 እገዛ፦ ብሔራዊ መታወቂያ በፎቶ ወይም በ PDF ሲልኩ በራስ-ሰር አስተካክሎ ይሰጣል። ማንኛውንም ጥያቄ እዚህ በመጻፍ ከ AI ጋር መነጋገር ይችላሉ።")
    elif user_text == "🛠 Admin Panel":
        bot.reply_to(message, "🔐 ይህ ለአድሚን ብቻ የተፈቀደ ክፍል ነው።")
    else:
        # ተጠቃሚው በተን ሳይሆን ተራ ፅሁፍ ሲጽፍ በ Gemini AI ይመለስለታል
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            response = ai_model.generate_content(user_text)
            bot.reply_to(message, response.text, parse_mode="Markdown")
        except Exception as e:
            # ፎርማት ስህተት ካመጣ ያለ ማርክዳውን በቴክስት ብቻ ለመላክ
            try:
                bot.reply_to(message, response.text)
            except:
                bot.reply_to(message, "🤖 ይቅርታ፣ አሁን ላይ ምላሽ መስጠት አልቻልኩም። እባክዎ ጥቂት ቆይተው ይሞክሩ።")

# ቦቱን ማስነሳት
print("አዲሱ ስማርት የቢዝነስ ቦት በተሳካ ሁኔታ ስራ ጀምሯል...")
bot.infinity_polling()
