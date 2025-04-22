# config.py – إعدادات ZadJannahBot الرسمية

# معلومات تشغيل البوت
BOT_TOKEN = "7800594975:AAFz7imbaTGAYvf-WhKxgIxBxrgpKEiIsVo"
ADMIN_ID = 585555633
ADMIN_USERNAME = "@osama_cfc"

# مسارات وقوائم
USERS_DB_PATH = "users.json"
ALL_USERS_CHAT_IDS = []

# الإعدادات العامة
TIMEZONE = "Asia/Riyadh"
DEFAULT_CITY = "الداير بني مالك"

# إعدادات الدعم الفني (اختياري)
SUPPORT_CHAT_ID = None  # ضع رقم ID للدعم أو اتركها None

# ميّزات البوت (قابلة للتفعيل أو الإيقاف)
FEATURE_TOGGLES = {
    "azkar": True,
    "quran": True,
    "duas": True,
    "quotes": True,
    "witr_reminder": True,
    "daily_deeds": True,
    "salat_times": True
}

# إصدار البوت
VERSION = "1.0.0"
