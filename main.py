import telebot
import json
import random
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, ALL_USERS_CHAT_IDS, USERS_DB_PATH

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل المستخدمين تلقائيًا
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

# أمر /start
@bot.message_handler(commands=['start'])
def start_message(message):
    register_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        "مرحبًا بك في ZadJannahBot!\nجعله الله زادًا لك إلى الجنة.\n\n"
        "ابدأ رحلتك مع الذكر من خلال القائمة، أو انتظر رسائلك اليومية تلقائيًا."
    )

# لوحة تحكم المشرف
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "أهلاً بك في لوحة التحكم.
كل شيء يعمل بنجاح.")
    else:
        bot.send_message(message.chat.id, "هذه اللوحة خاصة بالمشرف فقط.")

# رسالة يومية: أفعال بسيطة بأجور عظيمة
def send_daily_good_deed():
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
    markup.add(types.InlineKeyboardButton("طبقتها اليوم ✅", callback_data="applied_deed"))
    for user_id in ALL_USERS_CHAT_IDS:
        bot.send_message(user_id, f"✨ أفعال بسيطة بأجور عظيمة:

{deed}", reply_markup=markup)

# دعاء وفاء للوالدين
def send_parents_dua():
    duas = [
        "اللهم ارحم والديّ كما ربياني صغيرًا.",
        "اللهم اجعل والديّ من السعداء في الدنيا والآخرة.",
        "اللهم اغفر لوالديّ وبارك لهما في أعمارهم إن كانوا أحياء، وارحمهم إن كانوا أمواتًا.",
        "اللهم اجعل قبر والديّ روضة من رياض الجنة.",
        "اللهم اجعل دعائي لوالديّ نورًا يصل إليهم كل صباح ومساء.",
    ]
    dua = random.choice(duas)
    for user_id in ALL_USERS_CHAT_IDS:
        bot.send_message(user_id, f"**دعاء وفاء للوالدين**:

{dua}")

# استجابة زر "طبقتها اليوم ✅"
@bot.callback_query_handler(func=lambda call: call.data == "applied_deed")
def handle_applied_deed(call):
    bot.answer_callback_query(call.id, "ما شاء الله! رزقك الله القبول.")

print("البوت جاهز. انتظر بدء polling ...")
bot.infinity_polling()
