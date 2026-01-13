from telegram import BotCommand
from telegram.ext import CallbackQueryHandler, MessageHandler, filters
from telegram.ext._handlers.commandhandler import CommandHandler

from modules.configs import ALLOWED_USERS


def command(cmd, description, filter=filters.ALL, guest_allowed=False):
    def decorator(func):
        func.decorator_type = "command"
        func.cmd = cmd
        func.description = description

        final_filter = filter
        if guest_allowed:
            final_filter &= filters.User(user_id=ALLOWED_USERS)
        func.filter = final_filter
        return func

    return decorator


def callback(pattern):
    def decorator(func):
        func.decorator_type = "callback"
        func.pattern = pattern
        return func

    return decorator


def message(filter=filters.ALL, guest_allowed=False):
    def decorator(func):
        func.decorator_type = "message"

        final_filter = filter
        final_filter &= filters.TEXT
        if guest_allowed:
            final_filter &= filters.User(user_id=ALLOWED_USERS)
        func.filter = final_filter
        return func

    return decorator


class Handler:
    commands = []
    handlers = []

    def get_handlers(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "decorator_type"):
                if attr.decorator_type == "command":
                    self.commands.append(BotCommand(attr.cmd, attr.description))
                    self.handlers.append(
                        CommandHandler(attr.cmd, attr, filters=attr.filter)
                    )

                elif attr.decorator_type == "callback":
                    self.handlers.append(
                        CallbackQueryHandler(attr, pattern=attr.pattern)
                    )

                elif attr.decorator_type == "message":
                    self.handlers.append(
                        MessageHandler(filters=attr.filter, callback=attr)
                    )

        return self.commands, self.handlers
