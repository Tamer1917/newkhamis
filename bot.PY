import logging
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# إعدادات Firebase
cred = credentials.Certificate(r"C:\Users\LENOVO\Desktop\therapp\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# إعدادات التليجرام
TELEGRAM_TOKEN = "7996338110:AAGKkgFy1qpUQG4E9A4ZJrgc0aon4cx8JpI"
HTML_PAGE_URL = "https://wednsdaychess.vercel.app"

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# الدالة التي ستتم عند استقبال الرسائل
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    username = user.username if user.username else f"User{user_id}"  # في حالة عدم وجود اسم مستخدم
    # البحث عن المستخدم في قاعدة البيانات
    user_ref = db.collection('users').document(str(user_id))
    doc = user_ref.get()

    if doc.exists:
        # إذا كان المستخدم موجودًا بالفعل
        user_data = doc.to_dict()
        points = user_data.get("points", 0)
    else:
        # إذا كان المستخدم غير موجود
        points = 5  # إضافة 5 نقاط للمستخدم الجديد
        # إضافة المستخدم إلى قاعدة البيانات
        user_ref.set({
            'username': username,
            'points': points
        })

    # تكوين رابط صفحة HTML مع بيانات المستخدم
    url = f"{HTML_PAGE_URL}?username={username}&points={points}"
    
    # إرسال الرابط إلى المستخدم
    await update.message.reply_text(f"مرحبًا {username}!\nعدد النقاط: {points}\n\n📌 عرض التفاصيل: [اضغط هنا]({url})", parse_mode="Markdown")

# الدالة الرئيسية لتشغيل البوت
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    application.run_polling()

if __name__ == '__main__':
    main()
