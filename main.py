import telebot
import json
import random
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, USERS_DB_PATH, ALL_USERS_CHAT_IDS
import os
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل المستخدم
def register_user(user_id):
    try:
        with open(USERS_DB_PATH, "r") as f:
            users = json.load(f)
    except:
        users = []

    if user_id not in users:
        users.append({
            "id": user_id,
            "city": "غير محددة",
            "dhikr_count": 0,
            "witr": 0,
            "duha_days": 0,
            "last_dua": ""
        })
        with open(USERS_DB_PATH, "w") as f:
            json.dump(users, f)

# /start
@bot.message_handler(commands=['start'])
def start_message(message):
    register_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"مرحبًا {message.from_user.first_name}!
"
        "أنا ZadJannahBot – زادك إلى الجنة بإذن الله.

"
        "ابدأ رحلتك اليومية مع الأذكار والصلاة والدعاء.
"
        "سنذكرك دائمًا بكل خير!"
    )

# /myinfo
@bot.message_handler(commands=['myinfo'])
def my_info(message):
    user_id = message.from_user.id
    try:
        with open(USERS_DB_PATH, "r") as f:
            users = json.load(f)
        user_data = next((u for u in users if u.get("id") == user_id), None)
    except:
        user_data = {}

    city = user_data.get("city", "لم يتم تحديد المدينة")
    dhikr_count = user_data.get("dhikr_count", 0)
    witr_count = user_data.get("witr", 0)
    duha_days = user_data.get("duha_days", 0)
    last_dua = user_data.get("last_dua", "لا يوجد دعاء مسجل")

    reply = f"""
🧾 *ملخصك في ZadJannahBot*

• المدينة: {city}
• عدد الأذكار هذا الأسبوع: {dhikr_count}
• عدد ركعات الوتر: {witr_count}
• صلاة الضحى: {duha_days} يوم
• آخر دعاء ضغطته: {last_dua}

💡 استمر فالذكر حياة للقلب!
"""
    bot.send_message(message.chat.id, reply, parse_mode="Markdown")

# /deed
@bot.message_handler(commands=['deed'])
def send_daily_good_deed(message=None):
    deeds = [
        "تبسّمك في وجه أخيك صدقة.",
        "كفّ الأذى عن الطريق صدقة.",
        "قول 'سبحان الله وبحمده' 100 مرة تُغفر بها الذنوب.",
        "إفشاء السلام يُنشر المحبة.",
        "الوضوء قبل النوم أمان من الشيطان.",
        "الصلاة على النبي ﷺ عشر مرات، تنال بها عشر صلوات من الله.",
        "الاستغفار سبب للرزق، (فقلت استغفروا ربكم...) نوح: 10",
        "زيارة مريض، لك مثل أجر صائم قائم.",
        "سُقي كلبٌ فغفر الله له.",
        "رفع يدك بالدعاء = ثقة بالله.",
    ]
    deed = random.choice(deeds)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("طبقتها اليوم ✅", callback_data="applied_deed"),
        types.InlineKeyboardButton("ذكرني بها لاحقًا 🔔", callback_data="remind_later")
    )
    if message:
        bot.send_message(message.chat.id, f"✨ *فعل اليوم:*

{deed}", parse_mode="Markdown", reply_markup=markup)
    else:
        for user_id in ALL_USERS_CHAT_IDS:
            bot.send_message(user_id, f"✨ *فعل اليوم:*

{deed}", parse_mode="Markdown", reply_markup=markup)

# أزرار التفاعل
@bot.callback_query_handler(func=lambda call: call.data == "applied_deed")
def handle_applied_deed(call):
    bot.answer_callback_query(call.id, "ما شاء الله! رزقك الله القبول.")

@bot.callback_query_handler(func=lambda call: call.data == "remind_later")
def remind_later(call):
    bot.send_message(call.message.chat.id, "تمام! سأذكّرك بها لاحقًا إن شاء الله.")

print("البوت جاهز. انتظر بدء polling ...")
bot.infinity_polling()


# (تنبيهات أخرى، عداد الذكر، أذكار الصباح/المساء، دعاء الوالدين، وِتر، الضحى، استغفار منتصف الليل، الثلث الأخير، وغيرها)
# ستُدرج هنا كل الدوال والأزرار والجدولة النهائية...
