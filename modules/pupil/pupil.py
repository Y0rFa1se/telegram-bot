from typing import Type
from modules.base.handler import command, callback, Handler
from modules.base.tg_api import Utils, BotAPI, CallbackAPI
from modules.base.table import Table


class PupilHandler(Handler):
    def __init__(self):
        self.pupils = Table(
            "pupils", scheme={"text": str}, pk="text", not_null={"text"}
        )
        self.cursor = 0

    @command("hl", "pupil list")
    async def hl_cmd(self, update, context):
        self.cursor = 0
        keyboard = [
            [("Next", "pupil_hl_next")]
        ]
        reply_markup = Utils.inline_keyboard(keyboard)
        
        pupil_list = [pupil["text"] for pupil in self.pupils[self.cursor : self.cursor + 10]]
        
        await BotAPI.reply(
            update, context, "hl\n\n" + "\n".join(pupil_list), reply_markup=reply_markup
        )

    @command("ha", "pupil add")
    async def ha_cmd(self, update, context):
        args = await BotAPI.get_raw_args(update, context)
        if not args:
            await BotAPI.reply(update, context, "Usage: /ha <pupil_name>")
            return

        args = [{"text": Table.text_preproc(arg)} for arg in args]
        self.pupils << args
        await BotAPI.reply(update, context, "Pupil(s) added.")
            
    @command("hd", "pupil delete")
    async def hd_cmd(self, update, context):
        args = await BotAPI.get_raw_args(update, context)
        if not args:
            await BotAPI.reply(update, context, "Usage: /hd <pupil_name>")
            return

        for arg in args:
            pupil_name = Table.text_preproc(arg)
            if pupil_name in self.pupils:
                self.pupils >> pupil_name
                await BotAPI.reply(update, context, f"Pupil '{pupil_name}' deleted.")
            else:
                await BotAPI.reply(update, context, f"Pupil '{pupil_name}' not found.")
        ~self.pupils

    @command("hr", "pupil random")
    async def hr_cmd(self, update, context):
        keyboard = [
            [("sample", "pupil_hr_sample")]
        ]
        reply_markup = Utils.inline_keyboard(keyboard)
        args = await BotAPI.get_args(update, context)
        if args and args[0].isdigit():
            n = int(args[0])
            await BotAPI.reply(update, context, "\n".join(self.pupils % n), reply_markup=reply_markup)
            return
        await BotAPI.reply(update, context, (self.pupils % 1)[0], reply_markup=reply_markup)
        
    @command("hs", "pupil search")
    async def hs_cmd(self, update, context):
        args = await BotAPI.get_args(update, context)
        arg = args[0] if args else None
        if not arg:
            await BotAPI.reply(update, context, "Usage: /hs <substring>")
            return
        
        res = self.pupils @ arg
        await BotAPI.reply(update, context, "hs\n\n" + "\n".join(res))
        
    @command("hstart", "pupil startswith")
    async def hstart_cmd(self, update, context):
        args = await BotAPI.get_args(update, context)
        arg = args[0] if args else None
        if not arg:
            await BotAPI.reply(update, context, "Usage: /hstart <prefix>")
            return
        
        res = self.pupils ^ arg
        await BotAPI.reply(update, context, "hstart\n\n" + "\n".join(res))
        
    @command("hend", "pupil endswith")
    async def hend_cmd(self, update, context):
        args = await BotAPI.get_args(update, context)
        arg = args[0] if args else None
        if not arg:
            await BotAPI.reply(update, context, "Usage: /hend <suffix>")
            return
        
        res = self.pupils / arg
        await BotAPI.reply(update, context, "hend\n\n" + "\n".join(res))
        
    @callback("pupil_hl_next")
    async def pupil_hl_next_callback(self, update, context):
        query = await CallbackAPI.get_callback(update, context)
        self.cursor += 10
        keyboard = [
            [("Prev", "pupil_hl_prev"), ("Next", "pupil_hl_next")]
        ]
        reply_markup = Utils.inline_keyboard(keyboard)
        
        try:
            pupil_list = [pupil["text"] for pupil in self.pupils[self.cursor : self.cursor + 10]]
        except TypeError:
            pupil_list = []
            
        await CallbackAPI.edit(
            query,
            text="\n".join(pupil_list) if pupil_list else "No more pupils.",
            reply_markup=reply_markup,
        )
        
    @callback("pupil_hl_prev")
    async def pupil_hl_prev_callback(self, update, context):
        query = await CallbackAPI.get_callback(update, context)
        self.cursor = max(0, self.cursor - 10)
        keyboard = [
            [("Prev", "pupil_hl_prev"), ("Next", "pupil_hl_next")]
        ]
        reply_markup = Utils.inline_keyboard(keyboard)
        
        try:
            pupil_list = [pupil["text"] for pupil in self.pupils[self.cursor : self.cursor + 10]]
        except TypeError:
            pupil_list = []
        
        await CallbackAPI.edit(
            query,
            text="\n".join(pupil_list) if pupil_list else "No more pupils.",
            reply_markup=reply_markup,
        )
        
    @callback("pupil_hr_sample")
    async def pupil_hr_sample_callback(self, update, context):
        keyboard = [
            [("sample", "pupil_hr_sample")]
        ]
        reply_markup = Utils.inline_keyboard(keyboard)
        query = await CallbackAPI.get_callback(update, context)
        sample = (self.pupils % 1)[0]
        await CallbackAPI.edit(
            query,
            text=sample,
            reply_markup=reply_markup,
        )