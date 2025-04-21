import telebot
import json
import random
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, USERS_DB_PATH, ALL_USERS_CHAT_IDS
import os
from datetime import datetime
from scheduler import schedule_tasks  # تأكد أن scheduler.py موجود
from hijri_converter import convert

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل المستخدم
def register_user(user_id):
    try:
        with open(USERS_DB_PATH, "r") as f:
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
            "last_dua": ""
        }
        users.append(new_user)
        with open(USERS_DB_PATH, "w") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    # تحديث القائمة
    global ALL_USERS_CHAT_IDS
    ALL_USERS_CHAT_IDS = [u["id"] if isinstance(u, dict) else u for u in users]
    @bot.message_handler(commands=['start'])
def start_message(message):
    register_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"""مرحبًا {message.from_user.first_name}!
أنا ZadJannahBot – زادك إلى الجنة بإذن الله.

ابدأ رحلتك اليومية مع الأذكار والصلاة والدعاء.
سنذكرك دائمًا بكل خير!"""
    )

# أوامر البوت
bot.set_my_commands([
    types.BotCommand("start", "بدء البوت"),
    types.BotCommand("admin", "لوحة تحكم المشرف"),
    types.BotCommand("azkar", "أذكار الصباح والمساء"),
    types.BotCommand("salat_azkar", "أذكار بعد الصلاة"),
    types.BotCommand("sleep_azkar", "أذكار النوم"),
    types.BotCommand("witr", "تذكير بصلاة الوتر"),
    types.BotCommand("next_salah", "وقت الصلاة القادمة"),
    types.BotCommand("deed", "أفعال بأجور عظيمة"),
    types.BotCommand("parents", "دعاء للوالدين"),
    types.BotCommand("name", "اسم من أسماء الله الحسنى"),
    types.BotCommand("quote", "حكمة من أحد الصالحين"),
    types.BotCommand("dua", "دعاء للمسلمين"),
    types.BotCommand("khatmah", "الجزء القرآني اليومي"),
    types.BotCommand("hadith", "حديث اليوم"),
    types.BotCommand("myinfo", "ملفك الشخصي في ZadJannahBot")
])
# أذكار الصباح
def send_morning_azkar(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("أذكار مختصرة", callback_data="azkar_morning_short"),
        types.InlineKeyboardButton("أذكار كاملة", callback_data="azkar_morning_full")
    )
    bot.send_message(user_id, "☀️ *أذكار الصباح*\nاختر النسخة التي تفضلها:", parse_mode="Markdown", reply_markup=markup)

# أذكار المساء
def send_evening_azkar(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("أذكار مختصرة", callback_data="azkar_evening_short"),
        types.InlineKeyboardButton("أذكار كاملة", callback_data="azkar_evening_full")
    )
    bot.send_message(user_id, "🌙 *أذكار المساء*\nاختر النسخة التي تفضلها:", parse_mode="Markdown", reply_markup=markup)

# التعامل مع ضغط الأزرار
@bot.callback_query_handler(func=lambda call: call.data in [
    "azkar_morning_short", "azkar_morning_full",
    "azkar_evening_short", "azkar_evening_full"
])
def handle_azkar_buttons(call):
    azkar_data = {
        "azkar_morning_short": "☀️ *أذكار الصباح المختصرة:*\n- أصبحنا وأصبح الملك لله...\n- الحمد لله...\n- اللهم بك أصبحنا وبك نحيا...",
        "azkar_morning_full": "☀️ *أذكار الصباح الكاملة:*\n- آية الكرسي\n- المعوذات\n- أصبحنا وأصبح الملك لله...\n- اللهم ما أصبح بي من نعمة...\n- لا إله إلا الله وحده لا شريك له...\n- وأكثر من 10 أذكار أخرى...",
        "azkar_evening_short": "🌙 *أذكار المساء المختصرة:*\n- أمسينا وأمسى الملك لله...\n- الحمد لله...\n- اللهم بك أمسينا وبك نحيا...",
        "azkar_evening_full": "🌙 *أذكار المساء الكاملة:*\n- آية الكرسي\n- المعوذات\n- أمسينا وأمسى الملك لله...\n- اللهم ما أمسى بي من نعمة...\n- بسم الله الذي لا يضر مع اسمه شيء...\n- وأكثر من 10 أذكار أخرى...\n\n{خاتمة الأذكار: آخر آيتين من سورة البقرة}"
    }
    bot.send_message(call.message.chat.id, azkar_data[call.data], parse_mode="Markdown")
   # أذكار بعد الصلاة
@bot.message_handler(commands=['salat_azkar'])
def send_salat_azkar(message):
    text = """🕌 *أذكار بعد الصلاة:*

- أستغفر الله (3 مرات)
- اللهم أنت السلام ومنك السلام تباركت يا ذا الجلال والإكرام
- لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير
- سبحان الله (33) – الحمد لله (33) – الله أكبر (33)
- لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير

✨ الأذكار تحفظك وترفع درجاتك"""
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
# أذكار النوم
@bot.message_handler(commands=['sleep_azkar'])
def send_sleep_azkar(message):
    text = """🛌 *أذكار النوم:*

- باسمك ربي وضعت جنبي وبك أرفعه...
- اللهم قني عذابك يوم تبعث عبادك
- آية الكرسي
- سورة الإخلاص + الفلق + الناس
- سبحان الله (33) – الحمد لله (33) – الله أكبر (34)
- {خاتمة الأذكار: آخر آيتين من سورة البقرة}

✨ نم على طاعة، يُختم يومك بالذكر"""
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    # دعاء الاستعاذة للأبناء (يرسل مرتين يوميًا عبر scheduler)
def send_child_protection_dua(user_id):
    text = """🛡️ *دعاء الاستعاذة للأبناء:*

أُعيذكم بكلمات الله التامة من كل شيطان وهامة، ومن كل عين لامّة.

- [صحيح البخاري]"""
    bot.send_message(user_id, text, parse_mode="Markdown")
    @bot.message_handler(commands=['parents'])
def send_parents_dua(message):
    duas = [
        "اللهم ارحم والديّ كما ربياني صغيرًا.",
        "اللهم اجعل والديّ من السعداء في الدنيا والآخرة.",
        "اللهم اغفر لوالديّ وبارك لهما إن كانا أحياء، وارحمهما إن كانا أمواتًا.",
        "اللهم اجعل دعائي لوالديّ نورًا يصل إليهم كل صباح ومساء.",
        "اللهم اجعل قبر والديّ روضة من رياض الجنة."
    ]
    selected = random.choice(duas)
    bot.send_message(message.chat.id, f"❤️ *دعاء للوالدين:*\n\n{selected}", parse_mode="Markdown")
    @bot.message_handler(commands=['dua'])
def send_general_dua_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("دعاء للوالدين", callback_data="dua_parents"),
        types.InlineKeyboardButton("دعاء للأبناء", callback_data="dua_kids"),
        types.InlineKeyboardButton("دعاء للزوج/الزوجة", callback_data="dua_spouse"),
        types.InlineKeyboardButton("دعاء للمسلمين", callback_data="dua_muslims")
    )
    bot.send_message(message.chat.id, "اختر نوع الدعاء الذي ترغب به:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dua_"))
def handle_dua_buttons(call):
    categories = {
        "dua_parents": "اللهم اغفر لوالديّ وارزقني برّهم أحياءً وأمواتًا.",
        "dua_kids": "اللهم احفظ أبنائي وبناتي، وبارك لي فيهم.",
        "dua_spouse": "اللهم اجعل بيني وبين زوجي مودة ورحمة وسعادة دائمة.",
        "dua_muslims": "اللهم اغفر للمسلمين والمسلمات، الأحياء منهم والأموات."
    }
    text = categories.get(call.data, "دعاء مبارك")
    bot.send_message(call.message.chat.id, f"📿 *الدعاء المختار:*\n\n{text}", parse_mode="Markdown")
    @bot.message_handler(commands=['dhikr'])
def send_dhikr_counter(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    for count in [3, 10, 33, 99, 100]:
        markup.add(types.InlineKeyboardButton(f"{count} مرة", callback_data=f"count_{count}_0"))
    bot.send_message(message.chat.id, "اختر عدد مرات الذكر:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("count_"))
def handle_dhikr_count(call):
    parts = call.data.split("_")
    total = int(parts[1])
    current = int(parts[2]) + 1

    if current >= total:
        bot.answer_callback_query(call.id, text="اكتمل الذكر، تقبل الله منك!")
    else:
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(f"{current}/{total} اضغط", callback_data=f"count_{total}_{current}")
            )
        )
@bot.message_handler(commands=['name'])
def send_allah_name(message):
    names = [
        "الرحمن – كثير الرحمة بكل خلقه.",
        "الرحيم – رحمته خاصة بالمؤمنين.",
        "الغفور – يغفر الذنوب جميعًا.",
        "الشكور – يثيب القليل بالكثير.",
        "الرزاق – يرزق من يشاء بغير حساب.",
        "الودود – يحب عباده ويحبونه.",
        "اللطيف – يعلم دقائق الأمور ويرفق بعباده.",
        "الخبير – لا يخفى عليه شيء.",
        "الحي – لا يموت.",
        "القيوم – قائم على كل شيء بتدبيره."
    ]
    selected = random.choice(names)
    bot.send_message(message.chat.id, f"🌟 *اسم من أسماء الله الحسنى:*\n\n{selected}", parse_mode="Markdown")
    @bot.message_handler(commands=['quote'])
def send_salih_quote(message):
    quotes = [
        "قال أحد الصالحين: لا تنظر لصغر العمل، بل انظر لمن تعمل له.",
        "قال أحدهم: من أصلح سريرته، أصلح الله علانيته.",
        "قال أحدهم: من لم يشغل نفسه بالطاعة، شغلته بالمعصية.",
        "قال أحدهم: أحسن إلى الناس تستعبد قلوبهم.",
        "قال أحدهم: تزود للذي لا بد منه، فإن الموت ميقات العباد."
    ]
    selected = random.choice(quotes)
    bot.send_message(message.chat.id, f"📝 *قال أحد الصالحين:*\n\n{selected}", parse_mode="Markdown")
   @bot.message_handler(commands=['hadith'])
def send_daily_hadith(message):
    hadiths = [
        "قال رسول الله ﷺ: \"من صلى عليّ صلاة، صلى الله عليه بها عشرًا.\" – مسلم",
        "قال رسول الله ﷺ: \"من لا يشكر الناس لا يشكر الله.\" – الترمذي",
        "قال رسول الله ﷺ: \"الدال على الخير كفاعله.\" – الترمذي",
        "قال رسول الله ﷺ: \"إن الله لا ينظر إلى صوركم وأموالكم ولكن ينظر إلى قلوبكم وأعمالكم.\" – مسلم",
        "قال رسول الله ﷺ: \"اتق الله حيثما كنت.\" – الترمذي",
        "قال رسول الله ﷺ: \"يسروا ولا تعسروا، وبشروا ولا تنفروا.\" – البخاري",
        "قال رسول الله ﷺ: \"من حسن إسلام المرء تركه ما لا يعنيه.\" – الترمذي",
        "قال رسول الله ﷺ: \"أحب الناس إلى الله أنفعهم للناس.\" – صحيح الجامع",
        "قال رسول الله ﷺ: \"من قال لا إله إلا الله دخل الجنة.\" – البخاري",
        "قال رسول الله ﷺ: \"المسلم من سلم المسلمون من لسانه ويده.\" – البخاري"
    ]
    today = datetime.now().day
    index = today % len(hadiths)
    bot.send_message(message.chat.id, f"📜 *حديث اليوم:*\n\n{hadiths[index]}", parse_mode="Markdown")
@bot.message_handler(commands=['khatmah'])
def send_daily_khatmah(message):
    ayat = [
        "﴿ ذلك الكتاب لا ريب فيه ﴾ – البقرة",
        "﴿ سيقول السفهاء من الناس ﴾ – البقرة",
        "﴿ لن تنالوا البر حتى تنفقوا ﴾ – آل عمران",
        "﴿ يا أيها الذين آمنوا أوفوا بالعقود ﴾ – المائدة",
        "﴿ يا أيها الذين آمنوا لا تتخذوا اليهود والنصارى أولياء ﴾ – المائدة",
        "﴿ وإذا قرئ القرآن فاستمعوا له ﴾ – الأعراف",
        "﴿ أفمن شرح الله صدره للإسلام ﴾ – الزمر",
        "﴿ قد أفلح من تزكى ﴾ – الأعلى",
        "﴿ إن الله مع الذين اتقوا ﴾ – النحل",
        "﴿ إن أكرمكم عند الله أتقاكم ﴾ – الحجرات"
    ]
    hijri_day = convert.Gregorian.today().to_hijri().day
    index = hijri_day % len(ayat)
    bot.send_message(message.chat.id, f"📖 *جزء اليوم:*\n\n{ayat[index]}", parse_mode="Markdown")
    # تشغيل مهام الجدولة
schedule_tasks()
print("البوت جاهز. انتظر بدء polling ...")
bot.infinity_polling()
