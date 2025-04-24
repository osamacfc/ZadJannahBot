import os
import time
import json
import random
import logging
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
import requests
from telebot import types

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# إعدادات الجدولة
scheduler = BackgroundScheduler(timezone=timezone("Asia/Riyadh"))

# تخزين تفاعلات المستخدم
user_interactions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    register_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"مرحبًا {message.from_user.first_name}!\n"
        "أنا *ZadJannahBot* – زادك إلى الجنة بإذن الله.\n\n"
        "ابدأ رحلتك اليومية مع الأذكار والصلاة والدعاء.\n"
        "سنذكرك دائمًا بكل خير!",
        parse_mode="Markdown"
    )

# تسجيل المستخدم تلقائيًا
def register_user(user_id):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    existing_ids = [u["id"] if isinstance(u, dict) else u for u in users]

    if user_id not in existing_ids:
        new_user = {
            "id": user_id,
            "city": "غير محددة",
            "dhikr_count": 0,
            "witr": 0,
            "duha_days": 0,
            "last_dua": "",
            "last_seen": str(datetime.now())
        }
        users.append(new_user)
        with open("users.json", "w") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    global ALL_USERS_CHAT_IDS
    ALL_USERS_CHAT_IDS = [u["id"] if isinstance(u, dict) else u for u in users]

# إضافة تذكيرات للأذكار يومياً
def daily_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "تذكير بأذكار الصباح!")

# إضافة تذكير بالصلاة القادمة
def prayer_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "⏰ تذكير: الصلاة القادمة هي الفجر.")

# تحديث تفاعل المستخدم
def update_user_interaction(user_id, interaction_type):
    if user_id not in user_interactions:
        user_interactions[user_id] = {}
    if interaction_type not in user_interactions[user_id]:
        user_interactions[user_id][interaction_type] = 0
    user_interactions[user_id][interaction_type] += 1

# تعيين التذكير على مدار اليوم
scheduler.add_job(daily_reminder, 'cron', hour=6, minute=0)
scheduler.add_job(prayer_reminder, 'cron', hour=4, minute=30)

# دالة إظهار أوقات الصلاة للمستخدم
@bot.message_handler(commands=["get_prayer_times"])
def send_prayer_times(message):
    city = "مكة"  # هنا يُمكنك استبدالها بالمدينة المدخلة من المستخدم
    prayer_times = get_prayer_times(city)
    
    if prayer_times:
        response_text = f"مرحبًا {message.from_user.first_name}!\n\n"
        response_text += f"بناءً على موقعك في {city}، هذه هي أوقات الصلاة:\n"
        response_text += f"- الفجر: {prayer_times['Fajr']}\n"
        response_text += f"- الظهر: {prayer_times['Dhuhr']}\n"
        response_text += f"- العصر: {prayer_times['Asr']}\n"
        response_text += f"- المغرب: {prayer_times['Maghrib']}\n"
        response_text += f"- العشاء: {prayer_times['Isha']}\n"
        response_text += "نتمنى لك يومًا مباركًا!"
        bot.send_message(message.chat.id, response_text)
    else:
        bot.send_message(message.chat.id, "عذرًا، لم نتمكن من العثور على أوقات الصلاة للمدينة.")

# دالة لإستعلام أوقات الصلاة
def get_prayer_times(city):
    # استعلام الإحداثيات باستخدام Nominatim API
    location_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    response = requests.get(location_url)
    location_data = response.json()

    if location_data:
        latitude = location_data[0]["lat"]
        longitude = location_data[0]["lon"]

        # استعلام أوقات الصلاة باستخدام Aladhan API
        prayer_url = f"http://api.aladhan.com/v1/timings?latitude={latitude}&longitude={longitude}&method=2"
        prayer_response = requests.get(prayer_url)
        prayer_data = prayer_response.json()

        if prayer_data["code"] == 200:
            timings = prayer_data["data"]["timings"]
            return timings
        else:
            return None
    return None

# بدء الجدولة
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    else:
        return "Invalid request", 403

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    else:
        return "Invalid request", 403

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://zadjannahbot.onrender.com/")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
# زر عرض أوقات الصلاة
@bot.message_handler(commands=["get_prayer_times_button"])
def show_prayer_times_button(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("عرض أوقات الصلاة", callback_data="get_prayer_times")
    )
    bot.send_message(message.chat.id, "اضغط للحصول على أوقات الصلاة:", reply_markup=markup)
# دالة عرض أذكار الصباح المختصرة
@bot.message_handler(commands=['azkar'])
def show_azkar_options(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("☀️ أذكار الصباح (مختصرة)", callback_data="azkar_morning_short"),
        types.InlineKeyboardButton("☀️ أذكار الصباح (كاملة)", callback_data="azkar_morning_full"),
    )
    markup.add(
        types.InlineKeyboardButton("🌙 أذكار المساء (مختصرة)", callback_data="azkar_evening_short"),
        types.InlineKeyboardButton("🌙 أذكار المساء (كاملة)", callback_data="azkar_evening_full")
    )
    bot.send_message(message.chat.id, "اختر نوع الأذكار:", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == "azkar_morning_short")
def handle_short_morning(call):
    send_short_morning_azkar(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "azkar_morning_full")
def handle_full_morning(call):
    send_full_morning_azkar(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "azkar_evening_short")
def handle_short_evening(call):
    send_short_evening_azkar(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "azkar_evening_full")
def handle_full_evening(call):
    send_full_evening_azkar(call.message.chat.id)
def send_short_morning_azkar(user_id):
    short_morning_azkar = """☀️ *أذكار الصباح – مختصرة:* ... """
    bot.send_message(user_id, short_morning_azkar, parse_mode="Markdown")
short_morning_azkar = """1. *آية الكرسي:*  
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ، لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ... [البقرة: 255]

2. *سورة الإخلاص:*  
قُلْ هُوَ اللَّهُ أَحَدٌ، اللَّهُ الصَّمَدُ، لَمْ يَلِدْ وَلَمْ يُولَدْ، وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ.

3. *سورة الفلق:*  
قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ، مِن شَرِّ مَا خَلَقَ، وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ، وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ، وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ.

4. *سورة الناس:*  
قُلْ أَعُوذُ بِرَبِّ النَّاسِ، مَلِكِ النَّاسِ، إِلَٰهِ النَّاسِ، مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ، الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ، مِنَ الْجِنَّةِ وَالنَّاسِ.

5. *آخر آيتين من سورة البقرة:*  
آمَنَ الرَّسُولُ بِمَا أُنزِلَ إِلَيْهِ مِن رَبِّهِ وَالْمُؤْمِنُونَ...  
لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا... [البقرة: 285-286]

6. *أصبحنا وأصبح الملك لله...*  
أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير...

7. *رضيت بالله ربًا...*  
رضيت بالله ربًّا، وبالإسلام دينًا، وبمحمد ﷺ نبيًّا. (ثلاث مرات)

📚 *المصدر:* حصن المسلم – النصوص الكاملة."""
def send_short_morning_azkar(user_id):
    short_morning_azkar = """..."""  # الأذكار هنا
    bot.send_message(user_id, short_morning_azkar, parse_mode="Markdown")

# زر تفاعلي عند الضغط على "أذكار مختصرة"
@bot.callback_query_handler(func=lambda call: call.data == "azkar_morning_short")
def handle_short_morning_azkar(call):
    send_short_morning_azkar(call.message.chat.id)
  # دالة عرض أذكار الصباح الكاملة
def send_full_morning_azkar(user_id):
    full_morning_azkar = """
☀️ *أذكار الصباح – كاملة:*

1. *آية الكرسي:*  
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ، لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ، لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ... [البقرة: 255]

2. *سورة الإخلاص – 3 مرات:*  
قُلْ هُوَ اللَّهُ أَحَدٌ، اللَّهُ الصَّمَدُ، لَمْ يَلِدْ وَلَمْ يُولَدْ، وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ.

3. *سورة الفلق – 3 مرات:*  
قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ... (كاملة).

4. *سورة الناس – 3 مرات:*  
قُلْ أَعُوذُ بِرَبِّ النَّاسِ... (كاملة).

5. *أصبحنا وأصبح الملك لله...*

6. *اللهم بك أصبحنا وبك أمسينا...*

7. *رضيت بالله ربًا...* (ثلاث مرات)

8. *اللهم ما أصبح بي من نعمة...*

9. *اللهم عافني في بدني...* (ثلاث مرات)

10. *اللهم إني أسألك العفو والعافية...*

11. *اللهم إني أصبحت أشهدك...* (أربع مرات)

12. *حسبي الله لا إله إلا هو...* (سبع مرات)

13. *اللهم إني أعوذ بك من الهم والحزن...*

14. *اللهم إني أعوذ بك من الكفر والفقر...*

15. *اللهم إني أعوذ بك من الجبن والبخل...*

16. *اللهم إني أسألك علماً نافعًا...*

17. *استغفر الله العظيم وأتوب إليه.*

18. *سبحان الله وبحمده – 100 مرة*

19. *لا إله إلا الله وحده لا شريك له...* – 100 مرة

20. *آخر آيتين من سورة البقرة:*  
آمَنَ الرَّسُولُ...  
لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا... [البقرة: 285–286]

📚 *المصدر:* حصن المسلم – الصيغة الكاملة المعتمدة.
    """
    bot.send_message(user_id, full_morning_azkar, parse_mode="Markdown")

# زر تفاعلي عند الضغط على "أذكار كاملة"
@bot.callback_query_handler(func=lambda call: call.data == "azkar_morning_full")
def handle_full_morning_azkar(call):
    send_full_morning_azkar(call.message.chat.id)
  # دالة عرض أذكار المساء المختصرة
def send_short_evening_azkar(user_id):
    short_evening_azkar = """
🌙 *أذكار المساء – مختصرة:*

1. *آية الكرسي:*  
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ... [البقرة: 255]

2. *سورة الإخلاص*  
قُلْ هُوَ اللَّهُ أَحَدٌ، اللَّهُ الصَّمَدُ... (كاملة)

3. *سورة الفلق*  
قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ... (كاملة)

4. *سورة الناس*  
قُلْ أَعُوذُ بِرَبِّ النَّاسِ... (كاملة)

5. *آخر آيتين من سورة البقرة:*  
آمَنَ الرَّسُولُ...  
لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا... [البقرة: 285–286]

6. *أمسينا وأمسى الملك لله...*

7. *رضيت بالله ربًا...* (ثلاث مرات)

📚 *المصدر:* حصن المسلم – مختارة بصيغ كاملة
    """
    bot.send_message(user_id, short_evening_azkar, parse_mode="Markdown")

# زر تفاعلي عند الضغط على "أذكار المساء المختصرة"
@bot.callback_query_handler(func=lambda call: call.data == "azkar_evening_short")
def handle_short_evening_azkar(call):
    send_short_evening_azkar(call.message.chat.id)
  # دالة عرض أذكار المساء الكاملة
def send_full_evening_azkar(user_id):
    full_evening_azkar = """
🌙 *أذكار المساء – كاملة:*

1. *آية الكرسي* – [البقرة: 255]

2. *الإخلاص – 3 مرات*

3. *الفلق – 3 مرات*

4. *الناس – 3 مرات*

5. *أمسينا وأمسى الملك لله...*

6. *اللهم بك أمسينا وبك أصبحنا...*

7. *رضيت بالله ربًا...* – (ثلاث مرات)

8. *اللهم ما أمسى بي من نعمة...*

9. *اللهم عافني في بدني...* – (ثلاث مرات)

10. *اللهم إني أسألك العفو والعافية...*

11. *اللهم إني أمسيت أشهدك...* – (أربع مرات)

12. *حسبي الله لا إله إلا هو...* – (سبع مرات)

13. *اللهم إني أعوذ بك من الهم والحزن...*

14. *اللهم إني أعوذ بك من الكسل والعجز...*

15. *استغفر الله العظيم وأتوب إليه.*

16. *سبحان الله وبحمده – 100 مرة*

17. *لا إله إلا الله وحده لا شريك له...* – 100 مرة

18. *آخر آيتين من سورة البقرة* – [البقرة: 285–286]

📚 *المصدر:* حصن المسلم – الصيغة الكاملة
    """
    bot.send_message(user_id, full_evening_azkar, parse_mode="Markdown")

# زر تفاعلي عند الضغط على "أذكار المساء الكاملة"
@bot.callback_query_handler(func=lambda call: call.data == "azkar_evening_full")
def handle_full_evening_azkar(call):
    send_full_evening_azkar(call.message.chat.id)
# دوال أذكار النوم
def send_short_sleep_azkar(user_id):
    text = """
🛌 *أذكار النوم – مختصرة:*

1. *باسمك ربي وضعت جنبي وبك أرفعه، إن أمسكت نفسي فارحمها وإن أرسلتها فاحفظها.*

2. *اللهم باسمك أموت وأحيا.*

3. *اللهم قني عذابك يوم تبعث عبادك.*

4. *اللهم أسلمت نفسي إليك، وفوضت أمري إليك، وألجأت ظهري إليك...*

📚 *المصدر:* حصن المسلم
"""
    bot.send_message(user_id, text, parse_mode="Markdown")


def send_full_sleep_azkar(user_id):
    text = """
🛌 *أذكار النوم – كاملة:*

1. *آية الكرسي* – [البقرة: 255]  
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...

2. *الإخلاص – الفلق – الناس* (مرة واحدة لكل سورة)

3. *آخر آيتين من سورة البقرة – [285–286]*  
آمَنَ الرَّسُولُ...  
لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا...

4. *باسمك ربي وضعت جنبي وبك أرفعه...*

5. *اللهم قني عذابك يوم تبعث عبادك.*

6. *اللهم أسلمت نفسي إليك، ووجهت وجهي إليك...*  
(حديث البراء بن عازب – يُقال عند النوم على طهارة)

7. *استغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه.* – (ثلاث مرات)

8. *سبحان الله – الحمد لله – الله أكبر*  
(33 / 33 / 34 مرة على الترتيب)

📚 *المصدر:* حصن المسلم – الأذكار النبوية
"""
    bot.send_message(user_id, text, parse_mode="Markdown")
@bot.message_handler(commands=['sleep'])
def show_sleep_azkar(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🛌 أذكار النوم (مختصرة)", callback_data="sleep_short"),
        types.InlineKeyboardButton("🛌 أذكار النوم (كاملة)", callback_data="sleep_full")
    )
    bot.send_message(
        message.chat.id,
        "اختر نوع أذكار النوم التي تريد عرضها:",
        reply_markup=markup
    )
    bot.send_message(message.chat.id, "اختر نوع الأذكار:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "sleep_short")
def handle_sleep_short(call):
    send_short_sleep_azkar(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "sleep_full")
def handle_sleep_full(call):
    send_full_sleep_azkar(call.message.chat.id)
    # دوال أذكار بعد الصلاة
def send_short_salat_azkar(user_id):
    text = """
🕌 *أذكار بعد الصلاة – مختصرة:*

1. *أستغفر الله* – (ثلاث مرات)

2. *اللهم أنت السلام، ومنك السلام، تباركت يا ذا الجلال والإكرام.*

3. *لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير.*

📚 *المصدر:* حصن المسلم – مختصرة بعد كل صلاة
"""
    bot.send_message(user_id, text, parse_mode="Markdown")


def send_full_salat_azkar(user_id):
    text = """
🕌 *أذكار بعد الصلاة – كاملة:*

1. *أستغفر الله* – (ثلاث مرات)

2. *اللهم أنت السلام، ومنك السلام، تباركت يا ذا الجلال والإكرام.*

3. *لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير.*

4. *اللهم أعني على ذكرك وشكرك وحسن عبادتك.*

5. *سبحان الله – 33 مرة*  
*الحمد لله – 33 مرة*  
*الله أكبر – 34 مرة*

6. *قراءة آية الكرسي* – [البقرة: 255]  
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...

📚 *المصدر:* حصن المسلم – الصيغة الكاملة بعد كل صلاة
"""
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['salat_azkar'])
def show_salat_azkar(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🕌 أذكار الصلاة (مختصرة)", callback_data="salat_short"),
        types.InlineKeyboardButton("🕌 أذكار الصلاة (كاملة)", callback_data="salat_full")
    )
    bot.send_message(message.chat.id, "اختر نوع أذكار الصلاة:", reply_markup=markup)
    bot.send_message(message.chat.id, "اختر نوع الأذكار:", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == "salat_short")
def handle_salat_short(call):
    send_short_salat_azkar(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "salat_full")
def handle_salat_full(call):
    send_full_salat_azkar(call.message.chat.id)

# الآن دالة دعاء الوالدين، تبدأ بشكل مستقل تمامًا:
# دالة إرسال دعاء للوالدين
def send_parents_dua(user_id):
    duas = [
        "اللهم ارحم والدَيّ كما ربياني صغيرًا.",
        "اللهم اغفر لوالديّ، وارفع درجتهما في المهديين.",
        "اللهم اجعل قبريهما روضة من رياض الجنة.",
        "اللهم ارزق والديّ العفو والعافية والرضا.",
        "اللهم اجعل برّي بهما سببًا لدخولي الجنة.",
        "اللهم اجعل عملهما الصالح نورًا لهما في قبريهما.",
        "اللهم ارزقهما من حيث لا يحتسبان، وبارك في أعمارهم إن كانوا أحياء، وارحمهم إن كانوا أمواتًا.",
        "اللهم بلّغ أمي وأبي من الخير ما يتمنونه، واصرف عنهما كل سوء.",
        "اللهم اجمعني بهما في الفردوس الأعلى بغير حساب ولا عذاب.",
        "اللهم اجعل دعائي لوالديّ سببًا في رفع منزلتهم، وزدهم من الحسنات."
    ]
    selected = random.choice(duas)
    bot.send_message(user_id, f"❤️ *دعاء للوالدين:*\n\n{selected}", parse_mode="Markdown")

# أمر /parents – عرض زر دعاء الوالدين
@bot.message_handler(commands=['parents'])
def show_parents_dua_button(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("دعاء جديد للوالدين", callback_data="parents_dua")
    )
    bot.send_message(
        message.chat.id,
        "اختر دعاء جديد للوالدين:",
        reply_markup=markup
    )
    bot.send_message(
        message.chat.id,
        "اضغط الزر للحصول على دعاء متجدد للوالدين:",
        reply_markup=markup
    )

# تفعيل الزر التفاعلي
@bot.callback_query_handler(func=lambda call: call.data == "parents_dua")
def handle_parents_dua(call):
    send_parents_dua(call.message.chat.id)
@bot.callback_query_handler(func=lambda call: call.data == "parents_dua")
def handle_parents_dua(call):
    send_parents_dua(call.message.chat.id)

def send_family_dua(user_id, category):
    family_duas = {
        "kids": [
            "اللهم اجعلهم هداةً مهتدين، لا ضالين ولا مضلين.",
            "اللهم ارزقهم حبك وحب نبيك، والعمل بما يُرضيك.",
            "اللهم احفظهم من كل سوء، ووفقهم لما تحب وترضى.",
            "اللهم نوّر دربهم، ووسع رزقهم، وبارك في أعمارهم.",
            "اللهم اجعلهم من أهل القرآن وأهل الصلاح."
        ],
        "spouse": [
            "اللهم اجعلني قرة عين لزوجي/زوجتي، واجعله/اجعلها قرة عين لي.",
            "اللهم اجعل بيني وبين زوجي/زوجتي مودة ورحمة وسكينة.",
            "اللهم أصلح ذات بيننا، وبارك لنا في أعمارنا وأعمالنا."
        ],
        "siblings": [
            "اللهم احفظ إخواني وأخواتي، وبارك لي فيهم، وارزقنا برّ بعضنا.",
            "اللهم لا تريني فيهم بأسًا يبكيني، واشملهم بعنايتك.",
            "اللهم اجمعني بهم على الخير، ووفقهم لطاعتك."
        ],
        "family": [
            "اللهم احفظ عائلتي من كل سوء، وبارك لي فيهم.",
            "اللهم اجعلنا متحابين فيك، متعاونين على طاعتك.",
            "اللهم ارزقنا رضاك والجنة، واجعلنا من الشاكرين."
        ]
    }

    dua_list = family_duas.get(category, [])
    if dua_list:
        selected = random.choice(dua_list)
        bot.send_message(user_id, f"📿 *دعاء العائلة:*\n\n{selected}", parse_mode="Markdown")


@bot.message_handler(commands=['family'])
def show_family_dua_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("دعاء للأبناء", callback_data="family_kids"),
        types.InlineKeyboardButton("دعاء للزوج/الزوجة", callback_data="family_spouse")
    )
    markup.add(
        types.InlineKeyboardButton("دعاء للإخوان", callback_data="family_siblings"),
        types.InlineKeyboardButton("دعاء للعائلة", callback_data="family_family")
    )
    bot.send_message(message.chat.id, "اختر نوع الدعاء الذي تريده:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("family_"))
def handle_family_dua(call):
    category = call.data.replace("family_", "")
    send_family_dua(call.message.chat.id, category)


def send_kids_protection_dua(user_id):
    dua_text = """
👶 *دعاء الاستعاذة للأطفال:*

أُعِيذُكُمَا بِكَلِمَاتِ اللَّهِ التَّامَّةِ  
مِنْ كُلِّ شَيْطَانٍ وَهَامَّةٍ،  
وَمِنْ كُلِّ عَيْنٍ لَامَّةٍ.

📚 *الراوي:* عبد الله بن عباس رضي الله عنهما  
📘 *المصدر:* صحيح البخاري (3120)
"""
    bot.send_message(user_id, dua_text, parse_mode="Markdown")


@bot.message_handler(commands=['kids_dua'])
def show_kids_dua(message):
    send_kids_protection_dua(message.chat.id)


from apscheduler.schedulers.background import BackgroundScheduler

# تأكد من استيراد الوظيفة التي ترسل الدعاء:
def send_kids_protection_dua(uid):
    # من هنا سيقوم بإرسال الدعاء
    print(f"Sending protection dua to {uid}")

# إنشاء scheduler
scheduler = BackgroundScheduler()

# إضافة المهمة المجدولة
scheduler.add_job(
    lambda: [send_kids_protection_dua(uid) for uid in ALL_USERS_CHAT_IDS],
    trigger='cron', hour=7, minute=30
)

# بدء الـ scheduler
scheduler.start()
# دعاء الاستعاذة بالأبناء – قبل المغرب (17:15)
scheduler.add_job(
    lambda: [send_kids_protection_dua(uid) for uid in ALL_USERS_CHAT_IDS],
    trigger='cron', hour=17, minute=15
)


@bot.message_handler(commands=['dhikr'])
def show_dhikr_counter_options(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("3 مرات", callback_data="dhikr_3"),
        types.InlineKeyboardButton("10 مرات", callback_data="dhikr_10"),
        types.InlineKeyboardButton("33 مرة", callback_data="dhikr_33"),
        types.InlineKeyboardButton("100 مرة", callback_data="dhikr_100")
    )
    bot.send_message(message.chat.id, "اختر عدد التكرارات للذكر:", reply_markup=markup)


user_dhikr_state = {}


@bot.callback_query_handler(func=lambda call: call.data.startswith("dhikr_"))
def start_dhikr_tracking(call):
    count = int(call.data.replace("dhikr_", ""))
    user_dhikr_state[call.from_user.id] = {"target": count, "current": 0}

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("اذكر الآن", callback_data="dhikr_click"))
    bot.send_message(call.message.chat.id, f"اذكر الآن – {count} مرة\n\nاضغط على الزر مع كل تسبيحة.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "dhikr_click")
def handle_dhikr_click(call):
    user_id = call.from_user.id
    if user_id in user_dhikr_state:
        state = user_dhikr_state[user_id]
        state["current"] += 1

        if state["current"] >= state["target"]:
            bot.answer_callback_query(call.id, text="اكتمل الذكر! ما شاء الله.")
            bot.send_message(call.message.chat.id, "✅ تم الذكر بنجاح. أسأل الله أن يتقبل منك.")
            del user_dhikr_state[user_id]
        else:
            bot.answer_callback_query(call.id, text=f"عدّد الذكر: {state['current']} / {state['target']}")
    else:
        bot.answer_callback_query(call.id, text="ابدأ من /dhikr لاختيار العدد.")


random_duas = [
    "اللهم أعني على ذكرك وشكرك وحسن عبادتك.",
    "اللهم ارزقني رزقًا طيبًا واسعًا مباركًا.",
    "اللهم فرّج همّي ويسّر أمري واشرح صدري.",
    "اللهم اجعلني من التوابين واجعلني من المتطهرين.",
    "اللهم اجعل لي من كل همٍ فرجًا ومن كل ضيقٍ مخرجًا.",
    "اللهم اجعل عملي خالصًا لوجهك الكريم.",
    "اللهم ارزقني توبةً نصوحًا قبل الموت.",
    "اللهم اغفر لي ولوالدي وللمؤمنين يوم يقوم الحساب.",
    "اللهم يا مُقلّب القلوب ثبّت قلبي على دينك.",
    "اللهم إنك عفوٌ تحب العفو فاعفُ عني."
]


@bot.message_handler(commands=['dua'])
def send_random_dua(message):
    dua = random.choice(random_duas)
    bot.send_message(message.chat.id, f"📿 *دعاء اليوم:*\n\n{dua}", parse_mode="Markdown")


@bot.message_handler(commands=['share'])
def share_reward(message):
    bot.send_message(
        message.chat.id,
        "🔗 *شارك الأجر مع أصدقائك:*\n\n"
        "أرسل هذا الرابط لأي شخص ليبدأ رحلته مع الأذكار والدعاء:\n"
        "https://t.me/ZadJannah_Bot\n\n"
        "كل من استفاد بسببك، فلك مثل أجره بإذن الله.",
        parse_mode="Markdown"
    )


def send_witr_dua(user_id):
    witr_dua = """
🌙 *دعاء الوتر*:

اللهم إنا نرغب إليك في دعاء الوتر:

اللهم إني أعوذ برضاك من سخطك، وبمعافاتك من عقوبتك، وأعوذ بك منك، لا نحصي ثناءً عليك، أنت كما أثنيت على نفسك.

📚 *المصدر:* الحديث النبوي الصحيح.
    """
    bot.send_message(user_id, witr_dua, parse_mode="Markdown")


@bot.message_handler(commands=['witr'])
def send_witr_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("دعاء الوتر", callback_data="witr_dua")
    )
    bot.send_message(
        message.chat.id,
        "🌙 *صلاة الوتر* – ختام صلاتك ليلًا.\n\n"
        "أضف دعاء الوتر الآن!",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "witr_dua")
def handle_witr_dua(call):
    send_witr_dua(call.message.chat.id)
    
    if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://zadjannahbot.onrender.com/")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
