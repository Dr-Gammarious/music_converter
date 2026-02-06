from telegram import Update
from telegram.ext import ContextTypes

from handlers.audio_handler import sessions
from services.audio_processor import AudioProcessor
from utils.file_utils import remove_file


class TextHandler:
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        text = update.message.text

        if user_id not in sessions:
            await update.message.reply_text("لطفاً اول فایل صوتی بفرست.")
            return

        session = sessions[user_id]

        try:
            value = int(text)
        except ValueError:
            await update.message.reply_text("لطفاً فقط عدد وارد کن.")
            return

        # bit depth
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

        # sample rate reduction
        if session.sample_reduction is None:
            if value < 1 or value > 16:
                await update.message.reply_text(
                    "sample rate reduction باید بین 1 تا 16 باشه."
                )
                return

            session.sample_reduction = value

            await update.message.reply_text("در حال پردازش فایل ⏳")

            processor = AudioProcessor()
            output_path = processor.process(
                session.input_path,
                session.bit_depth,
                session.sample_reduction
            )

            await update.message.reply_audio(
                audio=open(output_path, "rb"),
                caption="فایل پردازش شده ✅"
            )

            # پاکسازی
            remove_file(session.input_path)
            remove_file(output_path)
            sessions.pop(user_id)

            return
