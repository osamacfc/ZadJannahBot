# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from telegram import Bot
from config import BOT_TOKEN, ADMIN_ID, TIMEZONE
import datetime

bot = Bot(token=BOT_TOKEN)
tz = timezone(TIMEZONE)

scheduler = BackgroundScheduler(timezone=tz)

def send_message(text, chat_id=ADMIN_ID):
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Error sending message: {e}")

def daily_tasks():
    now = datetime.datetime.now(tz)
    time_str = now.strftime("%I:%M %p")

    # مثال لرسائل يومية:
    send_message(f"☀️ صباح الخير!\nاذكر الله في هذا الصباح الجميل\n({time_str})")
    send_message("✨ أذكار الصباح متاحة الآن. لا تفوّتها!")
    send_message("❤️ دعاء للوالدين: اللهم ارحمهم كما ربّونا صغارًا.")
    send_message("سبحان الله وبحمده، سبحان الله العظيم.")

def schedule_tasks(updater=None):
    scheduler.add_job(daily_tasks, 'cron', hour=6, minute=30)  # كل يوم الساعة 6:30 صباحًا
    scheduler.start()

    if updater:
        updater.job_queue.run_once(lambda c: None, 1)  # ضروري للتكامل مع Updater
