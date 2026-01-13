from .configs import ENV, TOKEN
from .bot import Bot

from modules.test.test import TestHandler
from modules.pupil.pupil import PupilHandler


commands = []
handlers = []

if ENV == "DEV":
    test_handler = TestHandler()
    cmds, hnds = test_handler.get_handlers()
    commands.extend(cmds)
    handlers.extend(hnds)

pupil_handler = PupilHandler()
cmds, hnds = pupil_handler.get_handlers()
commands.extend(cmds)
handlers.extend(hnds)

bot = Bot(TOKEN, commands, handlers)
