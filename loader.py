from config import BOT_TOKEN

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import handlers

bot = Bot(token=BOT_TOKEN)
Bot.set_current(bot)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
Dispatcher.set_current(dp)
dp.middleware.setup(LoggingMiddleware())

handlers.setup(bot, dp)
