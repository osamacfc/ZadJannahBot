# handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from config import ADMIN_ID

def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    welcome_message = f"""
مرحبًا {user.first_name}!
أنا ZadJannahBot – زادك إلى الجنة بإذن الله.

ابدأ رحلتك اليومية مع الأذكار والصلاة والدعاء.  
سنذكّرك دائمًا بكل خير!
"""
    update.message.reply_text(welcome_message)

def admin_command(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("هذه اللوحة خاصة بالمشرف فقط.")
        return

    admin_panel = "لوحة التحكم:\n- إشراف التذكيرات\n- عدد المستخدمين\n- (تحديث قريبًا)"
    update.message.reply_text(admin_panel)

def setup_handlers(dp):
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("admin", admin_command))
