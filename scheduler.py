# === scheduler.py ===

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from telegram import Bot
from config import BOT_TOKEN, ADMIN_ID, TIMEZONE, ALL_USERS_CHAT_IDS
from datetime import datetime
from main import (
    send_morning_azkar,
    send_evening_azkar,
)

bot = Bot(token=BOT_TOKEN)
tz = timezone(TIMEZONE)
scheduler = BackgroundScheduler(timezone=tz)

def send_message(text):
    for user_id in ALL_USERS_CHAT_IDS:
        try:
            bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

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

    # صلاة الضحى (الساعة 9:00 صباحًا)
    scheduler.add_job(
        lambda: send_message("☀️ لا تنسَ صلاة الضحى! أقلها ركعتان، وأكثرها 8. أفضل وقتها بعد شروق الشمس بثلث ساعة."),
        trigger='cron', hour=9, minute=0
    )

    # تذكير الوتر (الساعة 11:45 مساءً)
    scheduler.add_job(
        lambda: send_message("🌙 لا تنسَ صلاة الوتر – ختام صلاتك ليلًا. عدد ركعاتها فردي."),
        trigger='cron', hour=23, minute=45
    )

    # استغفار منتصف الليل (12:30 صباحًا)
    scheduler.add_job(
        lambda: send_message("🕧 استغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه."),
        trigger='cron', hour=0, minute=30
    )

    # الثلث الأخير من الليل (2:30 صباحًا)
    scheduler.add_job(
        lambda: send_message("🌌 الثلث الأخير من الليل الآن – وقت نزول الرب، فاذكر الله واستغفر وادعُ."),
        trigger='cron', hour=2, minute=30
    )

    # قيام الليل (فجر الخميس فقط)
    scheduler.add_job(
        lambda: send_message("✨ هل اجتهدت في قيام الليل؟ ليلة الخميس من الليالي المباركة."),
        trigger='cron', day_of_week='thu', hour=4, minute=45
    )

    scheduler.start()
