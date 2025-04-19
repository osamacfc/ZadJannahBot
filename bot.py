import os
import time
import logging
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا بك في ZadJannahBot! جعله الله زادًا لك إلى الجنة.")

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(15)
