from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN
from handlers.start_handler import StartHandler
from handlers.audio_handler import AudioHandler
from handlers.text_handler import TextHandler


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = StartHandler()
    audio_handler = AudioHandler()
    text_handler = TextHandler()

    app.add_handler(CommandHandler("start", start_handler.handle))

    app.add_handler(
        MessageHandler(
            filters.AUDIO | filters.VOICE | filters.Document.ALL,
            audio_handler.handle
        )
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler.handle)
    )

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
