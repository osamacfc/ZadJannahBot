import os
import time
import logging
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
import requests
from telebot import types

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# حذف الـ Webhook
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

# تذكير بدعاء الجمعة قبل صلاة المغرب
def friday_last_hour_reminder():
    for user_id in user_interactions:
        bot.send_message(
            user_id,
            "⏰ تذكر دعاء يوم الجمعة: اللهم اجعلنا من أهل الجمعة الطيبة، واجعلها لنا بركة ورحمة، اللهم افتح لنا أبواب رحمتك، واغفر لنا ولأهلنا وأحبابنا، وارزقنا فيها من فضلك ما لا نحتسب، اللهم اجعلنا من الذين يستمعون القول فيتبعون أحسنه. اللهم ارزقنا الصلاة على نبيك محمد ﷺ في يوم الجمعة وفي كل يوم."
        )

# تعيين التذكير الساعة 5:00 مساءً قبل صلاة المغرب
scheduler.add_job(friday_last_hour_reminder, 'cron', day_of_week='fri', hour=17, minute=0)

# تذكير بفضل الدعاء في يوم الجمعة
def friday_prayer_reminder():
    for user_id in user_interactions:
        bot.send_message(
            user_id,
            "⏰ تذكر فضل الدعاء في يوم الجمعة: اللهم اجعلنا من أهل الدعاء المستجاب في هذا اليوم المبارك، واجعل دعائنا في هذا اليوم بركة لنا في الدنيا والآخرة."
        )

# تعيين التذكير الساعة 12:00 مساءً قبل زوال الشمس
scheduler.add_job(friday_prayer_reminder, 'cron', day_of_week='fri', hour=12, minute=0)

# تذكير بأذكار المساء
def evening_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "تذكير بأذكار المساء!")

# تعيين التذكير في الساعة 5:30 مساءً
scheduler.add_job(evening_reminder, 'cron', hour=17, minute=30)

# تذكير بالصلاة في الجماعة
def reminder_for_community_prayer():
    for user_id in user_interactions:
        bot.send_message(user_id, "تذكر الصلاة في المسجد مع الجماعة.")

# تعيين التذكير في الساعة 5:30 قبل صلاة المغرب
scheduler.add_job(reminder_for_community_prayer, 'cron', hour=17, minute=0)

# تذكير بالوضوء قبل الصلاة
def reminder_for_wudu():
    for user_id in user_interactions:
        bot.send_message(user_id, "تذكر الوضوء استعدادًا للصلاة.")

# تعيين التذكير قبل صلاة الفجر بساعة
scheduler.add_job(reminder_for_wudu, 'cron', hour=3, minute=30)

# تذكير بسورة الكهف يوم الجمعة
def reminder_for_surah_kaff():
    for user_id in user_interactions:
        bot.send_message(user_id, "تذكر قراءة سورة الكهف اليوم الجمعة!")

# تعيين التذكير قبل يوم الجمعة بساعات (مثلاً قبل يومين)
scheduler.add_job(reminder_for_surah_kaff, 'cron', day_of_week='thu', hour=12, minute=0)

# تعيين التفاعل مع الأذكار والدعاء
@bot.message_handler(commands=['azkar'])
def send_azkar(message):
    update_user_interaction(message.chat.id, "azkar")
    bot.send_message(message.chat.id, "أذكار الصباح: \n1. آية الكرسي\n2. سورة الإخلاص\n...")

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

# بدء الجدولة
scheduler.start()

# تشغيل البوت
def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(15)

run_bot()
