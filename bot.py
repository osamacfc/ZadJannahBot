import os
import time
import logging
from dotenv import load_dotenv
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone

# تحميل المتغيرات من ملف .env
load_dotenv()

# استخدام التوكن من متغير البيئة
TOKEN = os.getenv("TOKEN")

# إعداد البوت باستخدام التوكن
bot = telebot.TeleBot(TOKEN)

# تعطيل Webhook (لحل المشكلة التي ذكرتها)
bot.delete_webhook()


# إعدادات الجدولة
scheduler = BackgroundScheduler(timezone=timezone("Asia/Riyadh"))

# تخزين تفاعلات المستخدم
user_interactions = {}

# رسالة الترحيب عند بدء استخدام البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا بك في ZadJannahBot! جعله الله زادًا لك إلى الجنة.")

# تذكير بالأذكار يومياً
def daily_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "تذكير بأذكار الصباح!")

# تذكير بالصلاة القادمة
def prayer_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "⏰ تذكير: الصلاة القادمة هي الفجر.")

# تحديث تفاعل المستخدم
def update_user_interaction(user_id, interaction_type):
    if user_id not in user_interactions:
        user_interactions[user_id] = {}
    if interaction_type not in user_interactions[user_id]:
        user_interactions[user_id][interaction_type] = 0
    user_interactions[user_id][interaction_type] += 1

# تعيين التذكير على مدار اليوم
scheduler.add_job(daily_reminder, 'cron', hour=6, minute=0)
scheduler.add_job(prayer_reminder, 'cron', hour=4, minute=30)

# دالة التفاعل مع الأذكار
@bot.message_handler(commands=['azkar'])
def send_azkar(message):
    update_user_interaction(message.chat.id, "azkar")
    bot.send_message(message.chat.id, "أذكار الصباح: \n1. آية الكرسي\n2. سورة الإخلاص\n...")

# دالة التفاعل مع الدعاء
@bot.message_handler(commands=['dua'])
def send_dua(message):
    update_user_interaction(message.chat.id, "dua")
    bot.send_message(message.chat.id, "دعاء اليوم: \nاللهم اجعلني من أهل القرآن...")

# دالة الصلاة القادمة
@bot.message_handler(commands=['next_salah'])
def send_next_salah(message):
    update_user_interaction(message.chat.id, "next_salah")
    bot.send_message(message.chat.id, "⏰ الصلاة القادمة هي الفجر الساعة 4:30.")

# دالة صلاة الفجر
@bot.message_handler(commands=['fajr'])
def send_fajr(message):
    update_user_interaction(message.chat.id, "fajr")
    bot.send_message(message.chat.id, "⏰ صلاة الفجر قادمة الساعة 4:30.")

# تنفيذ الجدولة
scheduler.start()

# بدء البوت
def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(15)

run_bot()
