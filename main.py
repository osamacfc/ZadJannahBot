import telebot
import json
import random
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, USERS_DB_PATH

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل المستخدم تلقائيًا
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

# /start
@bot.message_handler(commands=['start'])
def start_message(message):
    register_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"مرحبًا {message.from_user.first_name}!\n"
        "أنا ZadJannahBot – زادك إلى الجنة بإذن الله.\n\n"
        "ابدأ رحلتك اليومية مع الأذكار والصلاة والدعاء.\n"
        "سندكُرك دائمًا بكل خير!"
    )

# /admin
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "لوحة التحكم:\n- كل شيء يعمل بنجاح.")
    else:
        bot.send_message(message.chat.id, "هذه اللوحة خاصة بالمشرف فقط.")

# /azkar
@bot.message_handler(commands=['azkar'])
def send_azkar(message):
    bot.send_message(message.chat.id, "☀️ أذكار الصباح والمساء:\n- الصباح بعد الشروق\n- المساء قبل الغروب")

# /salat_azkar
@bot.message_handler(commands=['salat_azkar'])
def send_salat_azkar(message):
    bot.send_message(message.chat.id, "🕌 أذكار بعد الصلاة:\n- استغفر الله (3)\n- سبحان الله (33)\n- الحمد لله (33)\n- الله أكبر (34)")

# /witr
@bot.message_handler(commands=['witr'])
def send_witr_reminder(message):
    bot.send_message(message.chat.id, "🌙 لا تنسَ صلاة الوتر!\nمن بعد العشاء حتى الفجر.")

# /next_salah
@bot.message_handler(commands=['next_salah'])
def next_salah(message):
    bot.send_message(message.chat.id, "⏰ قريبًا سيتم تفعيل ميزة معرفة وقت الصلاة القادمة بناءً على مدينتك.")

# /deed
@bot.message_handler(commands=['deed'])
def send_good_deed(message):
    deeds = [
        "تبسّمك في وجه أخيك صدقة.",
        "سبحان الله وبحمده 100 مرة = غُفرت ذنوبك.",
        "الوضوء قبل النوم أمان من الشيطان.",
        "إفشاء السلام يُنشر المحبة.",
        "الاستغفار يجلب الرزق والبركة.",
    ]
    deed = random.choice(deeds)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("طبقتها اليوم ✅", callback_data="applied_deed"))
    bot.send_message(message.chat.id, f"✨ فعل اليوم:\n{deed}", reply_markup=markup)

# /parents
@bot.message_handler(commands=['parents'])
def send_parents_dua(message):
    duas = [
        "اللهم ارحم والديّ كما ربياني صغيرًا.",
        "اللهم اجعل والديّ من السعداء في الدنيا والآخرة.",
        "اللهم اغفر لهما وبلّغهما منازل الصالحين.",
    ]
    bot.send_message(message.chat.id, random.choice(duas))

# /name
@bot.message_handler(commands=['name'])
def send_name(message):
    names = [
        "الرحمن: واسع الرحمة بعباده.",
        "الرحيم: رحيم بالمؤمنين.",
        "الغفور: يغفر الذنوب جميعًا.",
        "اللطيف: لطفه خفي وتدبيره عظيم.",
        "الرزاق: يرزق الخلق بلا حدود.",
    ]
    bot.send_message(message.chat.id, f"📛 اسم من أسماء الله:\n{random.choice(names)}")

# /quote
@bot.message_handler(commands=['quote'])
def send_quote(message):
    quotes = [
        "قال أحد الصالحين: لا تنظر لصغر العمل، بل انظر لمن تعمله.",
        "قال الشافعي: من لم تعزه التقوى فلا عز له.",
        "قال ابن القيم: كن في الدنيا كأنك عابر سبيل.",
    ]
    bot.send_message(message.chat.id, f"📜 {random.choice(quotes)}")

# /dua
@bot.message_handler(commands=['dua'])
def send_general_dua(message):
    bot.send_message(message.chat.id, "اللهم أصلح قلبي، واغفر ذنبي، ووفقني لطاعتك.")

# /khatmah
@bot.message_handler(commands=['khatmah'])
def send_quran_part(message):
    from datetime import datetime
    today = datetime.now()
    part = today.day  # مؤقتًا بالميلادي حتى نربطه هجريًا
    bot.send_message(message.chat.id, f"📖 الجزء القرآني اليوم:\nالجزء {part} من القرآن الكريم.")

# زر "طبقتها اليوم ✅"
@bot.callback_query_handler(func=lambda call: call.data == "applied_deed")
def handle_applied_deed(call):
    bot.answer_callback_query(call.id, "ما شاء الله! رزقك الله القبول.")

print("البوت يعمل الآن... ✅")
bot.infinity_polling()
