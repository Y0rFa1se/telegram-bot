from telegram.ext import ApplicationBuilder
import traceback


class Bot:
    app = None
    commands = []

    def __init__(self, token, commands, handlers):
        self.commands = commands
        
        self.app_builder = ApplicationBuilder().token(token)
        self.app_builder.post_init(self.set_commands)
        self.app = self.app_builder.build()

        for handler in handlers:
            self.app.add_handler(handler)

    def run(self):
        try:
            self.app.run_polling()
        except Exception:
            traceback.print_exc()

    async def set_commands(self, app):
        await app.bot.set_my_commands(self.commands)
        return
