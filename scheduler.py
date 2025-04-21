from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from telegram import Bot
from config import BOT_TOKEN, TIMEZONE, ALL_USERS_CHAT_IDS
import datetime

bot = Bot(token=BOT_TOKEN)
tz = timezone(TIMEZONE)
scheduler = BackgroundScheduler(timezone=tz)

# دالة إرسال للجميع
def send_message_to_all(text):
    for user_id in ALL_USERS_CHAT_IDS:
        try:
            bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"خطأ أثناء الإرسال إلى {user_id}: {e}")

# المهام اليومية في الصباح
def morning_tasks():
    now = datetime.datetime.now(tz)
    time_str = now.strftime("%I:%M %p")

    send_message_to_all(f"☀️ صباح الخير!\nاذكر الله في هذا الصباح الجميل\n({time_str})")
    send_message_to_all("✨ أذكار الصباح متاحة الآن. لا تفوّتها!")
    send_message_to_all("❤️ دعاء للوالدين: اللهم ارحمهم كما ربّونا صغارًا.")
    send_message_to_all("🌿 { سبحان الله وبحمده، سبحان الله العظيم }")

# تذكير منتصف الليل بالاستغفار
def midnight_istighfar():
    send_message_to_all("🌙 منتصف الليل! لحظة استغفار وهدوء...\nاستغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه.")

# تذكير الثلث الأخير من الليل
def last_third_of_night():
    send_message_to_all("⭐ الآن الثلث الأخير من الليل...\nينزل ربنا إلى السماء الدنيا\nفأكثروا من الدعاء والاستغفار وصلاة الوتر.")

# تفعيل المهام المجدولة
def schedule_tasks():
    # صباح الخير - الساعة 6:30 صباحًا
    scheduler.add_job(morning_tasks, 'cron', hour=6, minute=30)

    # استغفار منتصف الليل - الساعة 12:30 صباحًا
    scheduler.add_job(midnight_istighfar, 'cron', hour=0, minute=30)

    # الثلث الأخير من الليل (مثال: الساعة 3:45 صباحًا)
    scheduler.add_job(last_third_of_night, 'cron', hour=3, minute=45)

    scheduler.start()
    print("تم تشغيل المجدول اليومي – ZadJannahBot")
