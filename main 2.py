
import telebot
from telebot import types

# ضع هنا توكن البوت الخاص بك من BotFather
TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

# معرف المسؤول (استبدله بمعرفك الشخصي)
ADMIN_ID = 123456789

# رسالة الترحيب عند بدء البوت
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "مرحبًا بك في ZadJannahBot!\nجعله الله زادًا لك إلى الجنة.\n\n"
        "ابدأ رحلتك مع الذكر من خلال القائمة، أو انتظر رسائلك اليومية تلقائيًا."
    )

# لوحة التحكم للمسؤول
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "هذه اللوحة خاصة بالمشرف.")
        return

    bot.send_message(
        message.chat.id,
        "لوحة تحكم ZadJannahBot\n\n"
        "• عدد المستخدمين: قيد التفعيل\n"
        "• آخر التفاعلات: قريبًا\n"
        "• أوامر قيد التطوير..."
    )

# تشغيل البوت بشكل دائم
bot.polling(none_stop=True)
