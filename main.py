import os
import json
import random
import requests
from flask import Flask, request
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
from telebot import types
from data import (
    short_morning_azkar_full,
    full_morning_azkar_list,
    short_evening_azkar,
    full_evening_azkar_text,
    salat_azkar,
    full_salat_azkar,
    parents_duas,
    children_protection_dua,
    daily_deeds,
    salihin_quotes,
    daily_ahadith,
    azkar_sleep,
    names_of_allah,
    baqiyat_salihah,
    random_duas,
    nabd_dua_list,
    quran_parts,
    daily_verses
)

# رقم المشرف
ADMIN_ID = 585555633

# إعداد التوكن والبوت
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask app
app = Flask(__name__)

# إعداد الجدولة
scheduler = BackgroundScheduler(timezone=timezone("Asia/Riyadh"))

# تحميل المستخدمين من الملف
try:
    with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = []

ALL_USERS_CHAT_IDS = [u["id"] if isinstance(u, dict) else u for u in users]
user_interactions = {}

@bot.message_handler(commands=['azkar_sabah'])
def send_morning_azkar(message):
    # إرسال أذكار الصباح كاملة أو مختصرة
    bot.send_message(message.chat.id, "\n".join(short_morning_azkar_full))

@bot.message_handler(commands=['azkar_masaa'])
def send_evening_azkar(message):
    # إرسال أذكار المساء كاملة أو مختصرة
    bot.send_message(message.chat.id, full_evening_azkar_text)

@bot.message_handler(commands=['salat_azkar'])
def send_salat_azkar(message):
    # إرسال أذكار بعد الصلاة
    bot.send_message(message.chat.id, "\n".join(salat_azkar))

@bot.message_handler(commands=['parents_duas'])
def send_parents_duas(message):
    # إرسال دعاء الوالدين
    bot.send_message(message.chat.id, "\n".join(parents_duas))

@bot.message_handler(commands=['menu'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("أذكار الصباح")
    button2 = types.KeyboardButton("أذكار المساء")
    button3 = types.KeyboardButton("دعاء الوالدين")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "مرحبًا، اختر نوع الأذكار أو الدعاء:", reply_markup=markup)

@bot.message_handler(commands=['daily_verse'])
def send_daily_verse(message):
    # إرسال آية اليوم مع تفسيرها وفائدتها
    verse = daily_verses[0]  # يمكنك تعديل هذه لتكون عشوائية أو ديناميكية
    response = f"الآية: {verse['ayah']}\nالتفسير: {verse['tafseer']}\nالفائدة: {verse['faidah']}\nسبب النزول: {verse['sabab_nuzool']}\nالمصدر: {verse['source']}"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['random_dua'])
def send_random_dua(message):
    dua = random.choice(random_duas)  # اختيار دعاء عشوائي
    bot.send_message(message.chat.id, dua)


# دالة تسجيل المستخدم
def register_user(user_id):
    global ALL_USERS_CHAT_IDS
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
    ALL_USERS_CHAT_IDS = [u["id"] if isinstance(u, dict) else u for u in users]

# أمر /start
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

@bot.message_handler(commands=['admin'])
def show_admin_entry(message):
    if message.chat.id != ADMIN_ID:
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📊 فتح لوحة المشرف", callback_data="open_admin_panel"))
    bot.send_message(message.chat.id, "مرحبًا بك يا مشرف البوت.\nاضغط الزر لفتح لوحة التحكم.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "open_admin_panel")
def open_admin_panel(call):
    if call.message.chat.id != ADMIN_ID:
        return

    # تحميل المستخدمين
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
        total_users = len(users)
    except:
        total_users = "؟"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    response = f"""🔐 *لوحة تحكم المشرف*  
أهلًا بك مشرفي العزيز.  
• عدد المستخدمين الكلي: {total_users}  
• تاريخ التشغيل: `{now}`  
• ملاحظات: فقط أنت تملك صلاحية التحكم الكامل.

اختر إجراء من الأزرار أدناه:
"""

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👥 عدد المستخدمين", callback_data="admin_users"),
        types.InlineKeyboardButton("🟢 المتصلون الآن", callback_data="admin_active"),
        types.InlineKeyboardButton("📢 إرسال رسالة", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("🚨 تنبيه عاجل", callback_data="admin_alert")
    )
    bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    
# أذكار الصباح والمساء
def send_short_morning_azkar(user_id):
    text = "☀️ *أذكار الصباح – مختصرة:*\n1. آية الكرسي\n2. الإخلاص\n3. الفلق\n4. الناس"
    bot.send_message(user_id, text, parse_mode="Markdown")

def send_short_evening_azkar(user_id):
    text = "🌙 *أذكار المساء – مختصرة:*\n1. آية الكرسي\n2. الإخلاص\n3. الفلق\n4. الناس"
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['azkar'])
def show_azkar(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("☀️ أذكار الصباح", callback_data="morning"))
    markup.add(types.InlineKeyboardButton("🌙 أذكار المساء", callback_data="evening"))
    bot.send_message(message.chat.id, "اختر نوع الأذكار:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "morning")
def handle_morning(call):
    send_short_morning_azkar(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "evening")
def handle_evening(call):
    send_short_evening_azkar(call.message.chat.id)

# أذكار النوم
def send_sleep_azkar(user_id):
    text = "🛌 *أذكار النوم:*\n1. باسمك ربي وضعت جنبي...\n2. اللهم باسمك أموت وأحيا..."
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['sleep'])
def sleep_command(message):
    send_sleep_azkar(message.chat.id)

# دعاء الوتر
def send_witr_dua(user_id):
    text = "🌙 *دعاء الوتر:*\nاللهم إني أعوذ برضاك من سخطك، وبمعافاتك من عقوبتك..."
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['witr'])
def show_witr(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("دعاء الوتر", callback_data="witr_dua"))
    bot.send_message(message.chat.id, "اضغط لعرض دعاء الوتر:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "witr_dua")
def handle_witr(call):
    send_witr_dua(call.message.chat.id)

# عداد الذكر التفاعلي
user_dhikr_state = {}

@bot.message_handler(commands=['dhikr'])
def dhikr_start(message):
    markup = types.InlineKeyboardMarkup()
    for count in [3, 10, 33, 100]:
        markup.add(types.InlineKeyboardButton(f"{count} مرة", callback_data=f"dhikr_{count}"))
    bot.send_message(message.chat.id, "اختر عدد مرات الذكر:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dhikr_"))
def start_dhikr(call):
    count = int(call.data.split("_")[1])
    user_dhikr_state[call.from_user.id] = {"target": count, "current": 0}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("اذكر الآن", callback_data="dhikr_click"))
    bot.send_message(call.message.chat.id, f"اذكر الآن – {count} مرة", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "dhikr_click")
def dhikr_click(call):
    user_id = call.from_user.id
    if user_id in user_dhikr_state:
        state = user_dhikr_state[user_id]
        state["current"] += 1
        if state["current"] >= state["target"]:
            bot.send_message(call.message.chat.id, "✅ اكتمل الذكر! أسأل الله أن يتقبل.")
            del user_dhikr_state[user_id]
        else:
            bot.answer_callback_query(call.id, f"{state['current']} / {state['target']}")

# أذكار بعد الصلاة – مختصرة وكاملة
def send_short_salat_azkar(user_id):
    text = """
🕌 *أذكار بعد الصلاة – مختصرة:*
1. أستغفر الله (3 مرات)
2. اللهم أنت السلام ومنك السلام...
3. لا إله إلا الله وحده لا شريك له...
"""
    bot.send_message(user_id, text, parse_mode="Markdown")

def send_full_salat_azkar(user_id):
    text = """
🕌 *أذكار بعد الصلاة – كاملة:*
1. أستغفر الله (3 مرات)
2. اللهم أنت السلام ومنك السلام...
3. لا إله إلا الله وحده لا شريك له...
4. اللهم أعني على ذكرك وشكرك...
5. سبحان الله 33 – الحمد لله 33 – الله أكبر 34
6. آية الكرسي [البقرة: 255]
"""
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['salat_azkar'])
def salat_azkar_command(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🕌 مختصرة", callback_data="salat_short"),
        types.InlineKeyboardButton("🕌 كاملة", callback_data="salat_full")
    )
    bot.send_message(message.chat.id, "اختر نوع الأذكار بعد الصلاة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "salat_short")
def handle_salat_short(call):
    send_short_salat_azkar(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "salat_full")
def handle_salat_full(call):
    send_full_salat_azkar(call.message.chat.id)

# دعاء الوالدين
def send_parents_dua(user_id):
    duas = [
        "اللهم ارحم والدَيّ كما ربياني صغيرًا.",
        "اللهم اجعل قبريهما روضة من رياض الجنة.",
        "اللهم اجمعني بهما في الفردوس الأعلى."
    ]
    bot.send_message(user_id, f"❤️ *دعاء للوالدين:*\n\n{random.choice(duas)}", parse_mode="Markdown")

@bot.message_handler(commands=['parents'])
def parents_command(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("دعاء جديد", callback_data="parents_dua"))
    bot.send_message(message.chat.id, "اضغط الزر للحصول على دعاء جديد:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "parents_dua")
def handle_parents(call):
    send_parents_dua(call.message.chat.id)

# دعاء العائلة: الأبناء – الزوج – الإخوان – العائلة
def send_family_dua(user_id, category):
    family_duas = {
        "kids": [
            "اللهم اجعلهم هداةً مهتدين، لا ضالين ولا مضلين.",
            "اللهم ارزقهم حبك والعمل بما يُرضيك."
        ],
        "spouse": [
            "اللهم اجعل بيني وبين زوجي/زوجتي مودة ورحمة.",
            "اللهم أصلح ذات بيننا وبارك لنا."
        ],
        "siblings": [
            "اللهم احفظ إخواني وأخواتي وبارك لي فيهم.",
            "اللهم اجمعني بهم على طاعتك."
        ],
        "family": [
            "اللهم احفظ عائلتي من كل سوء.",
            "اللهم اجعلنا متحابين فيك متعاونين على طاعتك."
        ]
    }

    selected = random.choice(family_duas.get(category, []))
    bot.send_message(user_id, f"📿 *دعاء العائلة:*\n\n{selected}", parse_mode="Markdown")

@bot.message_handler(commands=['family'])
def family_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("دعاء للأبناء", callback_data="family_kids"))
    markup.add(types.InlineKeyboardButton("دعاء للزوج/الزوجة", callback_data="family_spouse"))
    markup.add(types.InlineKeyboardButton("دعاء للإخوان", callback_data="family_siblings"))
    markup.add(types.InlineKeyboardButton("دعاء للعائلة", callback_data="family_family"))
    bot.send_message(message.chat.id, "اختر نوع الدعاء:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("family_"))
def handle_family(call):
    category = call.data.replace("family_", "")
    send_family_dua(call.message.chat.id, category)

# دعاء الاستعاذة للأطفال
def send_kids_protection_dua(user_id):
    text = """
👶 *دعاء الاستعاذة للأطفال:*
أُعِيذُكُمَا بِكَلِمَاتِ اللَّهِ التَّامَّةِ  
مِنْ كُلِّ شَيْطَانٍ وَهَامَّةٍ،  
وَمِنْ كُلِّ عَيْنٍ لَامَّةٍ.
📘 *المصدر:* صحيح البخاري
"""
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['kids_dua'])
def kids_dua_command(message):
    send_kids_protection_dua(message.chat.id)
    # تحديث مدينة المستخدم
def update_user_city(user_id, city_name):
    for user in users:
        if isinstance(user, dict) and user["id"] == user_id:
            user["city"] = city_name
            with open("users.json", "w") as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            return True
    return False

# دالة جلب أوقات الصلاة من API
def get_prayer_times(city):
    try:
        # إحداثيات المدينة
        location_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        response = requests.get(location_url).json()
        if not response:
            return None
        lat, lon = response[0]["lat"], response[0]["lon"]
        # أوقات الصلاة
        prayer_url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
        prayer_data = requests.get(prayer_url).json()
        return prayer_data["data"]["timings"] if prayer_data["code"] == 200 else None
    except:
        return None

# أمر إدخال المدينة وحفظها
@bot.message_handler(commands=['get_prayer_times'])
def request_city(message):
    msg = bot.send_message(message.chat.id, "من فضلك أدخل اسم مدينتك:")
    bot.register_next_step_handler(msg, process_city_input)

def process_city_input(message):
    city = message.text.strip()
    prayer_times = get_prayer_times(city)
    if not prayer_times:
        bot.send_message(message.chat.id, "تعذر جلب أوقات الصلاة. حاول مجددًا.")
        return
    update_user_city(message.chat.id, city)
    show_prayer_times(message.chat.id, city, prayer_times)

# زر تفاعلي يعرض أوقات الصلاة
@bot.message_handler(commands=['get_prayer_times_button'])
def show_prayer_button(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("عرض أوقات الصلاة", callback_data="show_prayers"))
    bot.send_message(message.chat.id, "اضغط الزر لعرض أوقات الصلاة:", reply_markup=markup)

import requests

# المدن المخصصة بإحداثيات ثابتة
city_coords = {
    "الداير بني مالك": (17.30, 43.15),
    "فيفا": (17.25, 43.12),
    "العيدابي": (17.38, 42.99),
    "المدينة المنورة": (24.47, 39.61),
    "الرياض": (24.7136, 46.6753),
    "أبو ظبي": (24.4539, 54.3773),
    "الدوحة": (25.276987, 51.520008),
    "المنامة": (26.2235, 50.5822),
    "الكويت": (29.3759, 47.9774),
    "مسقط": (23.5880, 58.3829),
    "جدة": (21.4858, 39.1925),
    "مكة": (21.3891, 39.8579),
    "الشرقية": (26.4207, 50.0888)
}

# دالة جلب أوقات الصلاة بدقة عالية
def get_prayer_times(city):
    try:
        if city in city_coords:
            lat, lon = city_coords[city]
        else:
            location_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
            response = requests.get(location_url)
            location_data = response.json()
            if not location_data:
                return None
            lat = location_data[0].get("lat")
            lon = location_data[0].get("lon")
            if not lat or not lon:
                return None

        prayer_url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
        prayer_response = requests.get(prayer_url)
        prayer_data = prayer_response.json()

        if prayer_data["code"] == 200:
            return prayer_data["data"]["timings"]
        else:
            return None
    except Exception as e:
        print("خطأ أثناء جلب أوقات الصلاة:", e)
        return None

# عرض أوقات الصلاة للمستخدم
def show_prayer_times(user_id, city, times):
    response = f"📍 *أوقات الصلاة في {city.title()}*\n"
    response += f"• الفجر: {times['Fajr']}\n"
    response += f"• الشروق: {times['Sunrise']}\n"
    response += f"• الظهر: {times['Dhuhr']}\n"
    response += f"• العصر: {times['Asr']}\n"
    response += f"• المغرب: {times['Maghrib']}\n"
    response += f"• العشاء: {times['Isha']}\n"
    bot.send_message(user_id, response, parse_mode="Markdown")

def get_next_prayer_time(prayer_times):
    ksa = timezone('Asia/Riyadh')
    now = datetime.now(ksa).replace(second=0, microsecond=0)

    arabic_names = {
        "Fajr": "الفجر",
        "Sunrise": "الشروق",
        "Dhuhr": "الظهر",
        "Asr": "العصر",
        "Maghrib": "المغرب",
        "Isha": "العشاء"
    }

    suggestions = {
        "Fajr": "✨ لا تنسَ سنة الفجر، خيرٌ من الدنيا وما فيها.",
        "Sunrise": "☀️ وقت الضحى قد اقترب، صلاة الضحى كنز لا يفوّت.",
        "Dhuhr": "🕌 صلِّ الظهر بخشوع، فإنه أول صلاة أُقيمت في الإسلام.",
        "Asr": "⛅️ حافظ على العصر، فهي الصلاة الوسطى التي عظّمها الله.",
        "Maghrib": "🌇 لا تنسَ سنة المغرب، والدعاء في هذا الوقت مستجاب.",
        "Isha": "🌌 صلاة العشاء نور في القلب والوجه."
    }

    for name in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]:
        time_str = prayer_times.get(name)
        if not time_str:
            continue
        hour, minute = map(int, time_str.split(":"))
        prayer_time = now.replace(hour=hour, minute=minute)
        if prayer_time > now:
            remaining = prayer_time - now
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            if hours > 0:
                formatted = f"{hours} ساعة و{minutes} دقيقة"
            else:
                formatted = f"{minutes} دقيقة فقط"

            response = f"⏰ *الصلاة القادمة: {arabic_names[name]}*\n"
            response += f"• الوقت: {time_str}\n"
            response += f"• المتبقي: {formatted}\n"
            response += f"• التوصية: {suggestions[name]}"
            return response, name

    fajr_time = prayer_times.get("Fajr", "00:00")
    return f"⏰ *الصلاة القادمة: الفجر*\n• الوقت: {fajr_time}\n• المتبقي: بداية اليوم الجديد", "Fajr"
@bot.message_handler(commands=['next_salah'])
def send_next_salah(message):
    user_id = message.chat.id
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    user_city = next((u["city"] for u in users if u["id"] == user_id and isinstance(u, dict)), None)

    if not user_city or user_city == "غير محددة":
        bot.send_message(user_id, "من فضلك حدّد مدينتك أولاً باستخدام /get_prayer_times")
        return

    times = get_prayer_times(user_city)
    if times:
        response, prayer_key = get_next_prayer_time(times)
        markup = types.InlineKeyboardMarkup()
        if prayer_key == "Fajr":
            markup.add(types.InlineKeyboardButton("🌅 دعاء الاستيقاظ", callback_data="dua_wakeup"))
        elif prayer_key == "Maghrib":
            markup.add(types.InlineKeyboardButton("🌇 دعاء بين الأذان والإقامة", callback_data="dua_adhan"))
        elif prayer_key == "Isha":
            markup.add(types.InlineKeyboardButton("🌙 دعاء الوتر", callback_data="witr_dua"))
        else:
            markup.add(types.InlineKeyboardButton("📿 سنة أو دعاء", callback_data="general_sunnah"))

        bot.send_message(user_id, response, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(user_id, "تعذر جلب أوقات الصلاة حاليًا.")

@bot.callback_query_handler(func=lambda call: call.data == "show_prayers")
def handle_show_prayers_button(call):
    user_id = call.message.chat.id
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    user_city = next((u["city"] for u in users if u["id"] == user_id and isinstance(u, dict)), None)

    if not user_city or user_city == "غير محددة":
        bot.send_message(user_id, "من فضلك حدّد مدينتك أولاً باستخدام /get_prayer_times")
        return

    times = get_prayer_times(user_city)
    if times:
        response, prayer_key = get_next_prayer_time(times)
        markup = types.InlineKeyboardMarkup()
        if prayer_key == "Fajr":
            markup.add(types.InlineKeyboardButton("🌅 دعاء الاستيقاظ", callback_data="dua_wakeup"))
        elif prayer_key == "Maghrib":
            markup.add(types.InlineKeyboardButton("🌇 دعاء بين الأذان والإقامة", callback_data="dua_adhan"))
        elif prayer_key == "Isha":
            markup.add(types.InlineKeyboardButton("🌙 دعاء الوتر", callback_data="witr_dua"))
        else:
            markup.add(types.InlineKeyboardButton("📿 سنة أو دعاء", callback_data="general_sunnah"))

        bot.send_message(user_id, response, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(user_id, "تعذر جلب أوقات الصلاة.")

@bot.callback_query_handler(func=lambda call: call.data == "dua_wakeup")
def send_wakeup_dua(call):
    bot.send_message(call.message.chat.id, "🌅 *دعاء الاستيقاظ:*\nالحمد لله الذي أحيانا بعدما أماتنا وإليه النشور.", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "dua_adhan")
def send_between_adhan_dua(call):
    bot.send_message(call.message.chat.id, "🌇 *الدعاء بين الأذان والإقامة لا يُرد.*\nارفع يديك الآن واسأل الله من فضله.", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "general_sunnah")
def send_general_sunnah(call):
    bot.send_message(call.message.chat.id, "📿 *سنة نبوية اليوم:*\nصلِّ ركعتين قبل الظهر أو أكثر، فهي من أحب الأعمال إلى الله.", parse_mode="Markdown")
# استدعاء الأوقات عبر الزر التفاعلي
@bot.callback_query_handler(func=lambda call: call.data == "show_prayers")
def show_user_prayers(call):
    user_id = call.message.chat.id
    user_city = next((u["city"] for u in users if u["id"] == user_id and isinstance(u, dict)), None)
    if user_city and user_city != "غير محددة":
        times = get_prayer_times(user_city)
        if times:
            show_prayer_times(user_id, user_city, times)
        else:
            bot.send_message(user_id, "تعذر جلب أوقات الصلاة.")
    else:
        bot.send_message(user_id, "لم يتم تحديد مدينتك بعد. أرسل /get_prayer_times لتحديدها.")
        
    # تذكير أذكار الضحى (يُرسل بعد الشروق بـ20 دقيقة تقريبًا)
def send_duha_reminder():
    for u in users:
        if isinstance(u, dict):
            city = u.get("city")
            if not city or city == "غير محددة":
                continue
            times = get_prayer_times(city)
            if times:
                shurooq = times['Sunrise']
                hour, minute = map(int, shurooq.split(":"))
                duha_time = datetime.now().replace(hour=hour, minute=minute) + timedelta(minutes=20)
                now = datetime.now().replace(second=0, microsecond=0)
                if now.hour == duha_time.hour and now.minute == duha_time.minute:
                    bot.send_message(u["id"], "☀️ لا تنسَ صلاة الضحى، أجرها عظيم.")

# تذكير الاستعاذة بالأبناء (قبل المغرب بـ15 دقيقة تقريبًا)
def send_kids_protection_reminder():
    for u in users:
        if isinstance(u, dict):
            city = u.get("city")
            if not city or city == "غير محددة":
                continue
            times = get_prayer_times(city)
            if times:
                maghrib = times['Maghrib']
                hour, minute = map(int, maghrib.split(":"))
                reminder_time = datetime.now().replace(hour=hour, minute=minute) - timedelta(minutes=15)
                now = datetime.now().replace(second=0, microsecond=0)
                if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
                    send_kids_protection_dua(u["id"])
                    
# جدولة التذكيرات اليومية الذكية
scheduler.add_job(send_duha_reminder, 'cron', minute='*/1')  # مؤقت لتجريب التشغيل
scheduler.add_job(send_kids_protection_reminder, 'cron', minute='*/1')  # نفس الشي

# Webhook والتشغيل
@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.data.decode("utf-8"))
        bot.process_new_updates([update])
        return "", 200
    return "Invalid", 403

# قائمة البداية التفاعلية
@bot.message_handler(commands=['start'])
def show_main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("☀️ أذكار الصباح", callback_data="azkar_morning"),
        types.InlineKeyboardButton("🌙 أذكار المساء", callback_data="azkar_evening"),
        types.InlineKeyboardButton("❤️ دعاء الوالدين", callback_data="parents_dua"),
        types.InlineKeyboardButton("👨‍👩‍👧‍👦 دعاء العائلة", callback_data="family_dua"),
        types.InlineKeyboardButton("🛌 دعاء النوم", callback_data="sleep_dua"),
        types.InlineKeyboardButton("🌙 دعاء الوتر", callback_data="witr_dua"),
        types.InlineKeyboardButton("⏰ الصلاة القادمة", callback_data="next_salah"),
    )
    bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)


# قائمة الأذكار
@bot.message_handler(commands=['azkar'])
def show_azkar_options(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("☀️ أذكار الصباح", callback_data="azkar_morning_full"),
        types.InlineKeyboardButton("🌙 أذكار المساء", callback_data="azkar_evening_full"),
        types.InlineKeyboardButton("🛌 أذكار النوم", callback_data="sleep_full"),
        types.InlineKeyboardButton("🕌 بعد الصلاة", callback_data="salat_full")
    )
    bot.send_message(message.chat.id, "اختر نوع الأذكار:", reply_markup=markup)


# قائمة الأدعية
@bot.message_handler(commands=['dua'])
def show_dua_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📿 دعاء اليوم", callback_data="random_dua"),
        types.InlineKeyboardButton("❤️ دعاء الوالدين", callback_data="parents_dua"),
        types.InlineKeyboardButton("👨‍👩‍👧‍👦 دعاء العائلة", callback_data="family_family"),
        types.InlineKeyboardButton("👶 دعاء للأطفال", callback_data="kids_dua"),
        types.InlineKeyboardButton("🌙 دعاء الوتر", callback_data="witr_dua"),
        types.InlineKeyboardButton("📖 دعاء الأنبياء", callback_data="prophet_dua")
    )
    bot.send_message(message.chat.id, "اختر نوع الدعاء الذي تريده:", reply_markup=markup)


# عداد الذكر
@bot.message_handler(commands=['dhikr'])
def show_dhikr_counter(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✨ 3 مرات", callback_data="dhikr_3"),
        types.InlineKeyboardButton("✨ 10 مرات", callback_data="dhikr_10"),
        types.InlineKeyboardButton("✨ 33 مرة", callback_data="dhikr_33"),
        types.InlineKeyboardButton("✨ 100 مرة", callback_data="dhikr_100")
    )
    bot.send_message(message.chat.id, "اختر عدد تكرارات الذكر:", reply_markup=markup)


# قائمة الصيام
@bot.message_handler(commands=['sunnah_fasting'])
def show_sunnah_fasting(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🟣 الاثنين والخميس", callback_data="fast_mon_thu"),
        types.InlineKeyboardButton("⚪️ أيام البيض", callback_data="fast_white_days"),
        types.InlineKeyboardButton("🟡 يوم عرفة", callback_data="fast_arafah"),
        types.InlineKeyboardButton("🟠 يوم عاشوراء", callback_data="fast_ashura")
    )
    bot.send_message(message.chat.id, "اختر نوع الصيام للاطلاع على فضله:", reply_markup=markup)

scheduler.add_job(lambda: send_daily_dhikr("استغفر الله العظيم وأتوب إليه"), 'cron', hour='6,11,15,21')
scheduler.add_job(lambda: send_daily_dhikr("سبحان الله، الحمد لله، لا إله إلا الله، الله أكبر"), 'cron', hour='7,12,16,22')
scheduler.add_job(lambda: send_daily_dhikr("لا حول ولا قوة إلا بالله"), 'cron', hour='9,13,17,23')

def send_daily_dhikr(phrase):
    for u in users:
        if isinstance(u, dict):
            bot.send_message(u["id"], f"📿 {phrase}")

scheduler.add_job(lambda: send_salawat(), 'cron', hour='7,10,14,18,22')

def send_salawat():
    for u in users:
        if isinstance(u, dict):
            bot.send_message(u["id"], "اللهم صلِّ على محمد وعلى آل محمد كما صليت على إبراهيم...")

# كل ساعة يوم الجمعة
scheduler.add_job(lambda: send_salawat(), 'cron', day_of_week='fri', minute=0)

scheduler.add_job(lambda: send_kahf_reminder(), 'cron', day_of_week='fri', hour=6)
scheduler.add_job(lambda: send_last_hour_dua(), 'cron', day_of_week='fri', hour=17)

def send_kahf_reminder():
    for u in users:
        if isinstance(u, dict):
            bot.send_message(u["id"], "📖 لا تنسَ قراءة *سورة الكهف* اليوم.")

def send_last_hour_dua():
    for u in users:
        if isinstance(u, dict):
            bot.send_message(u["id"], "⏰ *الآن آخر ساعة من يوم الجمعة*، الدعاء فيها لا يُرد.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://zadjannahbot.onrender.com/")
    scheduler.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    # إرسال رسالة تأكيد للمشرف بعد التشغيل
    try:
        bot.send_message(ADMIN_ID, "✅ تم تشغيل البوت بنجاح يا إدمن!")
    except Exception as e:
        print("فشل إرسال رسالة الإدمن:", e)
