import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

import modules

ENV = os.getenv("APP_ENV", "DEV")

if ENV == "DEV":
    from dotenv import load_dotenv

    load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER = {int(os.getenv("ALLOWED_USER"))}


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello, {update.message.text}, {update.message.from_user.id}!"
    )
    return


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot is running...")

    try:
        app.run_polling()
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
