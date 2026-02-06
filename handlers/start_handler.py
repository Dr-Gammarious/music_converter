from telegram import Update
from telegram.ext import ContextTypes


class StartHandler:
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "سلام 👋\n"
            "لطفاً فایل صوتی خودت رو ارسال کن."
        )
