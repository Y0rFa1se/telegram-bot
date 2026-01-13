import telegram
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes


class Utils:
    @staticmethod
    def inline_keyboard(
        keyboard: list[list[tuple[str] | list[str]]],
    ) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text=txt, callback_data=callback)
                for txt, callback in row
            ]
            for row in keyboard
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def reply_keyboard(keyboard: list[list[str]]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


class BotAPI:
    @staticmethod
    async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return update.message.text

    @staticmethod
    async def get_args(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return context.args

    @staticmethod
    async def get_raw_args(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = await BotAPI.get_text(update, context)
        parts = text.split(maxsplit=1)
        if len(parts) <= 1:
            return []

        raw_args = parts[1].strip()
        args = [arg.strip() for arg in raw_args.split("\n")]

        return args

    @staticmethod
    async def reply(
        update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None
    ) -> telegram.Message:
        return await update.message.reply_text(text, reply_markup=reply_markup)

    @staticmethod
    async def edit(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        msg: telegram.Message = None,
        text: str = None,
        reply_markup=None,
    ) -> telegram.Message:
        try:
            target = msg if msg is not None else update.effective_message
            if not target:
                return None

            if text:
                return await target.edit_text(text, reply_markup=reply_markup)

            return await target.edit_reply_markup(reply_markup=reply_markup)

        except telegram.error.BadRequest as e:
            return None

    @staticmethod
    async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return await update.message.delete()

    @staticmethod
    async def delete_id(
        update: Update, context: ContextTypes.DEFAULT_TYPE, msg: telegram.Message
    ):
        return await context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=msg.message_id
        )


class CallbackAPI:
    @staticmethod
    async def get_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if query:
            await query.answer()

        return query

    @staticmethod
    async def reply(query: telegram.CallbackQuery, text: str, reply_markup=None):
        return await query.message.reply_text(text, reply_markup=reply_markup)

    @staticmethod
    async def edit(query: telegram.CallbackQuery, text: str = None, reply_markup=None):
        try:
            if text:
                return await query.edit_message_text(
                    text=text, reply_markup=reply_markup
                )

            return await query.edit_message_reply_markup(reply_markup=reply_markup)

        except telegram.error.BadRequest as e:
            return None

    @staticmethod
    async def delete(query: telegram.CallbackQuery):
        return await query.message.delete()
