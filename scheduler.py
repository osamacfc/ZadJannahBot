from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from config import BOT_TOKEN, ADMIN_ID, TIMEZONE, ALL_USERS_CHAT_IDS
from datetime import datetime
from telebot import TeleBot
from daily_tasks import (
    send_morning_azkar,
    send_evening_azkar,
    send_azkar_after_prayer,
    send_witr_reminder,
    send_sleep_azkar,
    send_witr_dua,
    send_duha_reminder,
    send_midnight_istighfar,
    send_last_third_night,
)

# تهيئة البوت مباشرة من التوكن بدون الرجوع إلى main.py
bot = TeleBot(BOT_TOKEN)
tz = timezone(TIMEZONE)
scheduler = BackgroundScheduler(timezone=tz)

# دالة لإرسال رسالة إلى جميع المستخدمين
def send_message(text):
    for user_id in ALL_USERS_CHAT_IDS:
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

# جدولة المهام التلقائية
def schedule_tasks():
    # أذكار الصباح
    scheduler.add_job(
        lambda: [send_morning_azkar(uid) for uid in ALL_USERS_CHAT_IDS],
        trigger='cron', hour=6, minute=0
    )

    # أذكار المساء
    scheduler.add_job(
        lambda: [send_evening_azkar(uid) for uid in ALL_USERS_CHAT_IDS],
        trigger='cron', hour=17, minute=30
    )

    # أذكار بعد الصلاة
    scheduler.add_job(
        lambda: [send_azkar_after_prayer(uid) for uid in ALL_USERS_CHAT_IDS],
        trigger='cron', hour=10, minute=0
    )

    # تذكير الوتر
    scheduler.add_job(
        send_witr_reminder,
        trigger='cron', hour=23, minute=30
    )

    # أذكار النوم
    scheduler.add_job(
        send_sleep_azkar,
        trigger='cron', hour=22, minute=0
    )

    # صلاة الضحى
    scheduler.add_job(
        lambda: send_message("☀️ لا تنسَ صلاة الضحى! أقلها ركعتان وأكثرها 8. أفضل وقتها بعد الشروق بثلث ساعة."),
        trigger='cron', hour=9, minute=0
    )

    # استغفار منتصف الليل
    scheduler.add_job(
        lambda: send_message("🕧 استغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه."),
        trigger='cron', hour=0, minute=30
    )

    # الثلث الأخير من الليل
    scheduler.add_job(
        lambda: send_message("🌌 الثلث الأخير من الليل الآن – وقت نزول الرب، فاذكر الله واستغفر وادعُ."),
        trigger='cron', hour=2, minute=30
    )

    # دعاء الوتر
    scheduler.add_job(
        send_witr_dua,
        trigger='cron', hour=23, minute=45
    )

    # الصلاة في جماعة
    scheduler.add_job(
        lambda: send_message("تذكر الصلاة في المسجد مع الجماعة"),
        trigger='cron', hour=5, minute=30
    )

    # تنبيه الفجر
    scheduler.add_job(
        lambda: send_message("⏰ صلاة الفجر قادمة. استعد للوضوء!"),
        trigger='cron', hour=4, minute=30
    )

    # تنبيه الصلاة القادمة
    scheduler.add_job(
        lambda: send_message("⏰ الصلاة القادمة هي: [الصلاة القادمة]"),
        trigger='cron', hour=6, minute=15
    )

    # قيام ليلة الخميس
    scheduler.add_job(
        lambda: send_message("🕯️ لا تنسَ قيام الليل ليلة الخميس!"),
        trigger='cron', hour=1, minute=0
    )

# بدء الجدولة
schedule_tasks()
scheduler.start()

# بدء البوت
def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(15)

run_bot()
