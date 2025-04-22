from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from telegram import Bot
from config import BOT_TOKEN, ADMIN_ID, TIMEZONE, ALL_USERS_CHAT_IDS
from datetime import datetime
from main import (
    send_morning_azkar,
    send_evening_azkar,
    send_witr_reminder,
    send_sleep_azkar,
    send_azkar_after_prayer,
    send_witr_dua,
    send_duha_reminder,
    send_midnight_istighfar,
    send_last_third_night,
)

bot = Bot(token=BOT_TOKEN)
tz = timezone(TIMEZONE)
scheduler = BackgroundScheduler(timezone=tz)

# Function to send a message to all users
def send_message(text):
    for user_id in ALL_USERS_CHAT_IDS:
        try:
            bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

# وظيفة لتحديد تذكير الصلاة و الأذكار
def schedule_tasks():
    # أذكار الصباح (الساعة 6:00 صباحًا)
    scheduler.add_job(
        lambda: [send_morning_azkar(uid) for uid in ALL_USERS_CHAT_IDS],
        trigger='cron', hour=6, minute=0
    )

    # أذكار المساء (الساعة 17:30 مساءً)
    scheduler.add_job(
        lambda: [send_evening_azkar(uid) for uid in ALL_USERS_CHAT_IDS],
        trigger='cron', hour=17, minute=30
    )

    # أذكار بعد الصلاة
    scheduler.add_job(
        lambda: [send_azkar_after_prayer(uid) for uid in ALL_USERS_CHAT_IDS],
        trigger='cron', hour=10, minute=0  # يتم تعديل هذا التوقيت حسب التوقيت الشرعي
    )

    # تذكير بالوتر
    scheduler.add_job(
        lambda: send_witr_reminder(),
        trigger='cron', hour=23, minute=30  # تعديل الوقت حسب الحاجة
    )

    # أذكار النوم
    scheduler.add_job(
        lambda: send_sleep_azkar(),
        trigger='cron', hour=22, minute=0  # تعديل الوقت حسب الحاجة
    )

    # صلاة الضحى (الساعة 9:00 صباحًا)
    scheduler.add_job(
        lambda: send_message("☀️ لا تنسَ صلاة الضحى! أقلها ركعتان، وأكثرها 8. أفضل وقتها بعد شروق الشمس بثلث ساعة."),
        trigger='cron', hour=9, minute=0
    )

    # دعاء الاستغفار منتصف الليل (12:30 صباحًا)
    scheduler.add_job(
        lambda: send_message("🕧 استغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه."),
        trigger='cron', hour=0, minute=30
    )

    # تذكير الثلث الأخير من الليل (2:30 صباحًا)
    scheduler.add_job(
        lambda: send_message("🌌 الثلث الأخير من الليل الآن – وقت نزول الرب، فاذكر الله واستغفر وادعُ."),
        trigger='cron', hour=2, minute=30
    )

    # التذكير بدعاء الوتر
    scheduler.add_job(
        lambda: send_witr_dua(),
        trigger='cron', hour=23, minute=45
    )

    # تذكير بالصلاة في جماعة
    scheduler.add_job(
        lambda: send_message("تذكر الصلاة في المسجد مع الجماعة"),
        trigger='cron', hour=5, minute=30  # قبل الصلاة
    )

    # تذكير صلاة الفجر (على حسب التوقيت الشرعي)
    scheduler.add_job(
        lambda: send_message("⏰ صلاة الفجر قادمة. استعد للوضوء!"),
        trigger='cron', hour=4, minute=30  # تعديل الوقت حسب التوقيت الشرعي
    )

    # تحديث الصلاة القادمة بناءً على أوقات الصلاة الشرعية
    scheduler.add_job(
        lambda: send_message("⏰ الصلاة القادمة هي: [الصلاة القادمة]"),
        trigger='cron', hour=6, minute=15
    )

    # صلاة قيام الليل في الخميس
    scheduler.add_job(
        lambda: send_message("✨ هل اجتهدت في قيام الليل؟ ليلة الخميس من الليالي المباركة."),
        trigger='cron', day_of_week='thu', hour=4, minute=45
    )

    scheduler.start()
