from telegram import Update
from telegram.ext import ContextTypes
from models.user_session import UserSession

# وضعیت کاربران (خیلی ساده)
sessions = {}


class AudioHandler:
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id

        file = None
        if update.message.audio:
            file = update.message.audio
        elif update.message.voice:
            file = update.message.voice
        elif update.message.document:
            file = update.message.document

        if not file:
            await update.message.reply_text("فایل صوتی معتبر نیست.")
            return

        telegram_file = await file.get_file()
        input_path = f"input_{user_id}.audio"
        await telegram_file.download_to_drive(input_path)

        session = UserSession()
        session.input_path = input_path
        sessions[user_id] = session

        await update.message.reply_text(
            "فایل دریافت شد ✅\n"
            "bit depth رو بین 1 تا 16 وارد کن:"
        )
