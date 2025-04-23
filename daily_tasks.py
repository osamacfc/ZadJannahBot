from main import bot, ALL_USERS_CHAT_IDS

def send_morning_azkar(user_id):
    text = """☀️ *أذكار الصباح – مختصرة:*

1. آية الكرسي [البقرة: 255]
2. سورة الإخلاص – 3 مرات
3. سورة الفلق – 3 مرات
4. سورة الناس – 3 مرات
5. أصبحنا وأصبح الملك لله...
6. اللهم بك أصبحنا وبك أمسينا...
7. رضيت بالله ربًا... (ثلاث مرات)

📚 *المصدر:* حصن المسلم
"""
    bot.send_message(user_id, text, parse_mode="Markdown")

def send_evening_azkar(user_id):
    text = """🌙 *أذكار المساء – مختصرة:*

1. آية الكرسي [البقرة: 255]
2. سورة الإخلاص – 3 مرات
3. سورة الفلق – 3 مرات
4. سورة الناس – 3 مرات
5. أمسينا وأمسى الملك لله...
6. اللهم بك أمسينا وبك أصبحنا...
7. رضيت بالله ربًا... (ثلاث مرات)

📚 *المصدر:* حصن المسلم
"""
    bot.send_message(user_id, text, parse_mode="Markdown")

def send_witr_reminder():
    for uid in ALL_USERS_CHAT_IDS:
        bot.send_message(uid, "🌙 لا تنسَ صلاة الوتر قبل النوم.")

def send_sleep_azkar():
    text = """🛌 *أذكار النوم:*

- باسمك ربي وضعت جنبي وبك أرفعه.
- اللهم باسمك أموت وأحيا.
- اللهم قني عذابك يوم تبعث عبادك.

📚 *المصدر:* حصن المسلم
"""
    for uid in ALL_USERS_CHAT_IDS:
        bot.send_message(uid, text, parse_mode="Markdown")

def send_azkar_after_prayer(user_id):
    text = """🕌 *أذكار بعد الصلاة – مختصرة:*

1. أستغفر الله – ثلاث مرات
2. اللهم أنت السلام، ومنك السلام، تباركت يا ذا الجلال والإكرام.
3. لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير.

📚 *المصدر:* حصن المسلم
"""
    bot.send_message(user_id, text, parse_mode="Markdown")

def send_witr_dua():
    text = """🌙 *دعاء الوتر:*

اللهم إنا نرغب إليك في دعاء الوتر:

اللهم إني أعوذ برضاك من سخطك، وبمعافاتك من عقوبتك، وأعوذ بك منك، لا نحصي ثناءً عليك، أنت كما أثنيت على نفسك.

📚 *المصدر:* الحديث النبوي الصحيح.
"""
    for uid in ALL_USERS_CHAT_IDS:
        bot.send_message(uid, text, parse_mode="Markdown")

def send_duha_reminder():
    for uid in ALL_USERS_CHAT_IDS:
        bot.send_message(uid, "☀️ لا تنسَ صلاة الضحى! أقلها ركعتان، وأكثرها 8.")

def send_midnight_istighfar():
    for uid in ALL_USERS_CHAT_IDS:
        bot.send_message(uid, "🕧 استغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه.")

def send_last_third_night():
    for uid in ALL_USERS_CHAT_IDS:
        bot.send_message(uid, "🌌 الثلث الأخير من الليل – وقت نزول الرب، فاذكر الله واستغفر وادعُ.")
