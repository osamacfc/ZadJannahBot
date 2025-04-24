import os
import logging
import telebot
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone

# إعداد البوت
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
WEBHOOK_URL = "https://zadjannahbot.onrender.com/"  # رابط Webhook النهائي

# إعداد Flask
app = Flask(__name__)

# إعداد Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# إعداد الجدولة
scheduler = BackgroundScheduler(timezone=timezone("Asia/Riyadh"))
scheduler.start()

# تخزين تفاعلات المستخدمين
user_interactions = {}

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id not in user_interactions:
        user_interactions[user_id] = {"joined": True}
    bot.send_message(user_id, "مرحبًا بك في ZadJannahBot! جعله الله زادًا لك إلى الجنة.")

# تحديث تفاعل المستخدم
def update_user_interaction(user_id, interaction_type):
    if user_id not in user_interactions:
        user_interactions[user_id] = {}
    user_interactions[user_id][interaction_type] = user_interactions[user_id].get(interaction_type, 0) + 1

# أوامر إضافية
@bot.message_handler(commands=['azkar'])
def send_azkar(message):
    update_user_interaction(message.chat.id, "azkar")
    bot.send_message(message.chat.id, "أذكار الصباح: \n1. آية الكرسي\n2. سورة الإخلاص\n...")

@bot.message_handler(commands=['dua'])
def send_dua(message):
    update_user_interaction(message.chat.id, "dua")
    bot.send_message(message.chat.id, "دعاء اليوم: \nاللهم اجعلني من أهل القرآن...")

@bot.message_handler(commands=['next_salah'])
def send_next_salah(message):
    update_user_interaction(message.chat.id, "next_salah")
    bot.send_message(message.chat.id, "⏰ الصلاة القادمة هي الفجر الساعة 4:30.")

@bot.message_handler(commands=['fajr'])
def send_fajr(message):
    update_user_interaction(message.chat.id, "fajr")
    bot.send_message(message.chat.id, "⏰ صلاة الفجر قادمة الساعة 4:30.")

# مهام التذكير
def daily_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "☀️ تذكير: لا تنسَ أذكار الصباح!")

def prayer_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "⏰ تذكير: الصلاة القادمة هي الفجر.")

def friday_last_hour_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "⏰ تذكر دعاء يوم الجمعة...")

def friday_prayer_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "⏰ تذكر فضل الدعاء في يوم الجمعة...")

def evening_reminder():
    for user_id in user_interactions:
        bot.send_message(user_id, "🌙 تذكير بأذكار المساء!")

def reminder_for_community_prayer():
    for user_id in user_interactions:
        bot.send_message(user_id, "صلاتك في الجماعة تزيد الأجر!")

def reminder_for_wudu():
    for user_id in user_interactions:
        bot.send_message(user_id, "لا تنس الوضوء قبل الصلاة.")

def reminder_for_surah_kaff():
    for user_id in user_interactions:
        bot.send_message(user_id, "سورة الكهف نور ما بين الجمعتين.")

# جدولة التذكيرات
scheduler.add_job(daily_reminder, 'cron', hour=6, minute=0)
scheduler.add_job(prayer_reminder, 'cron', hour=4, minute=30)
scheduler.add_job(friday_last_hour_reminder, 'cron', day_of_week='fri', hour=17, minute=0)
scheduler.add_job(friday_prayer_reminder, 'cron', day_of_week='fri', hour=12, minute=0)
scheduler.add_job(evening_reminder, 'cron', hour=17, minute=30)
scheduler.add_job(reminder_for_community_prayer, 'cron', hour=17, minute=0)
scheduler.add_job(reminder_for_wudu, 'cron', hour=3, minute=30)
scheduler.add_job(reminder_for_surah_kaff, 'cron', day_of_week='thu', hour=12, minute=0)

# نقطة استقبال Webhook
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid request', 403

# تشغيل التطبيق
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
