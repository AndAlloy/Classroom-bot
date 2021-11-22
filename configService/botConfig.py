from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from configService import registrationConfig, scheduleConfig
import os

bot = Bot(token=os.environ['TOKEN'])

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def menuHandler(callback_query):
    if callback_query.data == 'change_group':
        await registrationConfig.change_group(callback_query)
    elif callback_query.data == 'add_lesson':
        await scheduleConfig.inputSchedule(callback_query)
    elif callback_query.data == 'show_schedule':
        await scheduleConfig.getSchedule(callback_query)
