from telegram import Update
from telegram.ext import ContextTypes
from handlers.audio_handler import sessions


class TextHandler:
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        text = update.message.text

        if user_id not in sessions:
            await update.message.reply_text(
                "لطفاً اول یک فایل صوتی ارسال کن."
            )
            return

        session = sessions[user_id]

        # تلاش برای تبدیل متن به عدد
        try:
            value = int(text)
        except ValueError:
            await update.message.reply_text("لطفاً فقط عدد وارد کن.")
            return

        # مرحله دریافت bit depth
        if session.bit_depth is None:
            if value < 1 or value > 16:
                await update.message.reply_text(
                    "bit depth باید بین 1 تا 16 باشه."
                )
                return

            session.bit_depth = value

            await update.message.reply_text(
                "bit depth ذخیره شد ✅\n"
                "حالا sample rate reduction رو بین 1 تا 16 وارد کن:"
            )
            return

        # مرحله دریافت sample rate reduction
        if session.sample_reduction is None:
            if value < 1 or value > 16:
                await update.message.reply_text(
                    "sample rate reduction باید بین 1 تا 16 باشه."
                )
                return

            session.sample_reduction = value

            await update.message.reply_text(
                "اعداد دریافت شد ✅\n"
                "در حال پردازش فایل..."
            )

            # پردازش در فاز بعد اینجا صدا زده میشه
            return
