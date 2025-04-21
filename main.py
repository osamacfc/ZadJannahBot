import telebot
import json
import random
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, ALL_USERS_CHAT_IDS, USERS_DB_PATH

bot = telebot.TeleBot(BOT_TOKEN)

def register_user(user_id):
    try:
        with open(USERS_DB_PATH, "r") as f:
            users = json.load(f)
    except:
        users = []
    if user_id not in users:
        users.append(user_id)
        with open(USERS_DB_PATH, "w") as f:
            json.dump(users, f)

@bot.message_handler(commands=['start'])
def start_message(message):
    register_user(message.chat.id)
    bot.send_message(message.chat.id, "مرحبًا بك في ZadJannahBot!\nجعله الله زادًا لك إلى الجنة.\n\nابدأ رحلتك مع الذكر من خلال القائمة، أو انتظر رسائلك اليومية تلقائيًا.")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "لوحة التحكم:\n- عرض المتابعين\n- إرسال تنبيه عام...")
    else:
        bot.send_message(message.chat.id, "هذه اللوحة خاصة بالمشرف فقط.")

@bot.message_handler(commands=['azkar'])
def send_azkar(message):
    bot.send_message(message.chat.id, "☀️ أذكار الصباح والمساء:\n- أذكار متنوعة متجددة يوميًا")

@bot.message_handler(commands=['salat_azkar'])
def salat_azkar(message):
    bot.send_message(message.chat.id, "⏱️ أذكار بعد الصلاة:\n- لا تنس أذكارك بعد الصلوات")

@bot.message_handler(commands=['witrr'])
def witrr(message):
    bot.send_message(message.chat.id, "🌙 لا تنسَ صلاة الوتر قبل النوم.")

@bot.message_handler(commands=['next_salah'])
def next_salah(message):
    bot.send_message(message.chat.id, "🔔 الوقت المتبقي للصلاة القادمة: (هذه ميزة مستقبلية حسب التوقيت)")

@bot.message_handler(commands=['deed'])
def deed(message):
    deeds = ["قول سبحان الله وبحمده 100 مرة", "ابتسامة صدقة", "الوضوء قبل النوم..."]
    bot.send_message(message.chat.id, f"✨ فعل اليوم:\n{random.choice(deeds)}")

@bot.message_handler(commands=['parents'])
def parents(message):
    bot.send_message(message.chat.id, "اللهم اغفر لوالدينا وارحمهم كما ربونا صغارًا.")

@bot.message_handler(commands=['name'])
def name(message):
    bot.send_message(message.chat.id, "اسم اليوم من أسماء الله الحسنى: الرحمن - كثير الرحمة بعباده.")

@bot.message_handler(commands=['quote'])
def quote(message):
    bot.send_message(message.chat.id, "قال أحد الصالحين: لا تنظر لصغر العمل، بل انظر لمن تعمله.")

@bot.message_handler(commands=['dua'])
def dua(message):
    bot.send_message(message.chat.id, "دعاء اليوم: اللهم ارزقنا الإخلاص في القول والعمل.")

@bot.message_handler(commands=['khatmah'])
def khatmah(message):
    bot.send_message(message.chat.id, "📖 الجزء القرآني لليوم: الجزء 5 (حسب اليوم الهجري)")

bot.infinity_polling()
