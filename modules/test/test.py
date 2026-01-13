from modules.base.handler import command, callback, Handler
from modules.base.tg_api import Utils, BotAPI, CallbackAPI

class TestHandler(Handler):
    @command("rep", "Reply with the same message")
    async def rep_cmd(self, update, context):
        await BotAPI.reply(update, context, "안녕하세요")
        await BotAPI.reply(update, context, "안녕하세요")
        return
    
    @command("del", "Delete this command message")
    async def del_cmd(self, update, context):
        del_msg = await BotAPI.reply(update, context, "This command message will be deleted.")
        await BotAPI.delete(update, context)
        await BotAPI.delete_id(update, context, del_msg)
        return
    
    @command("edit", "Edit the command message")
    async def edit_cmd(self, update, context):
        msg = await BotAPI.reply(update, context, "This message will be edited.")
        await BotAPI.edit(update, context, msg, "This message has been edited.")
        return
    
    @command("inkey", "Show keyboard")
    async def inkey_cmd(self, update, context):
        keyboard = [
            [("Test", "test"), ("Help", "help")],
        ]
        markup = Utils.inline_keyboard(keyboard)
        await BotAPI.reply(update, context, "Choose an option:", markup)
        return
    
    @command("repkey", "Show reply keyboard")
    async def repkey_cmd(self, update, context):
        keyboard = [
            ["Option 1", "Option 2"],
            ["Option 3"],
        ]
        markup = Utils.reply_keyboard(keyboard)
        await BotAPI.reply(update, context, "Choose an option:", markup)
        return
    
    @callback("help")
    async def help_callback(self, update, context):
        query = await CallbackAPI.get_callback(update, context)
        await CallbackAPI.edit(query, text="This is the help section.")
        return