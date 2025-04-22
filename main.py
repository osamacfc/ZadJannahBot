import telebot
import json
import random
import os
from datetime import datetime
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, USERS_DB_PATH, ALL_USERS_CHAT_IDS
from scheduler import schedule_tasks

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل المستخدم تلقائيًا
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
            "last_dua": "",
            "last_seen": str(datetime.now())
        }
        users.append(new_user)
        with open(USERS_DB_PATH, "w") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    global ALL_USERS_CHAT_IDS
    ALL_USERS_CHAT_IDS = [u["id"] if isinstance(u, dict) else u for u in users]

# أمر /start – رسالة ترحيبية
@bot.message_handler(commands=["start"])
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

# إعداد قائمة الأوامر
bot.set_my_commands([
    types.BotCommand("start", "بدء البوت"),
    types.BotCommand("azkar", "أذكار الصباح والمساء"),
    types.BotCommand("sleep", "أذكار النوم"),
    types.BotCommand("salat_azkar", "أذكار بعد الصلاة"),
    types.BotCommand("deed", "أفعال بأجور عظيمة"),
    types.BotCommand("witr", "تذكير بالوتر + دعاءه"),
    types.BotCommand("name", "اسم من أسماء الله الحسنى"),
    types.BotCommand("dua", "دعاء عشوائي"),
    types.BotCommand("quote", "قال أحد الصالحين"),
    types.BotCommand("khatmah", "جزء اليوم من القرآن"),
    types.BotCommand("next_salah", "الصلاة القادمة"),
    types.BotCommand("myinfo", "ملفك الشخصي"),
    types.BotCommand("support", "الدعم والإعدادات")
])
# دالة عرض أذكار الصباح المختصرة
def send_short_morning_azkar(user_id):
    short_morning_azkar = """
☀️ *أذكار الصباح – مختصرة:*

1. *آية الكرسي:*  
اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ، لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ، لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ... [البقرة: 255]

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

📚 *المصدر:* حصن المسلم – النصوص الكاملة.
    """
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
  
