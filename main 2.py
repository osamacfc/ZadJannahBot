# main.py

from scheduler import schedule_tasks
from handlers import setup_handlers
from telegram.ext import Updater
from config import BOT_TOKEN

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # إعداد الأوامر والردود
    setup_handlers(dp)

    # جدولة الرسائل التلقائية
    schedule_tasks(updater)

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
