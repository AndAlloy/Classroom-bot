from aiogram import types
from aiogram.utils.exceptions import Throttled

import configService.keyboardsConfig as kb
from configService.botConfig import dp, bot
from model.base import Session
from model.user import User


async def start(message):
    try:
        await dp.throttle('start', rate=1)
    except Throttled:
        await message.reply('Too many requests!')
    else:
        session = Session()
        newUser = User(message)
        found = session.query(User) \
            .filter(User.telegramId == newUser.telegramId) \
            .all()
        if not found:
            session.add(newUser)
            session.commit()
            session.close()
        else:
            session.close()
        await message.reply('Hello!\nPlease choose subgroup:', reply_markup=kb.chooseKeyboard)


async def saveUser(callback_query, number):
    await types.ChatActions.typing()
    session = Session()
    newUser = User(callback_query)
    found = session.query(User) \
        .filter(User.telegramId == newUser.telegramId) \
        .first()
    found.subgroup = number
    session.commit()
    session.close()


async def change_group(callback_query):
    await types.ChatActions.typing()
    session = Session()
    newUser = User(callback_query)
    found = session.query(User) \
        .filter(User.telegramId == newUser.telegramId) \
        .first()
    session.close()

    await bot.send_message(callback_query.from_user.id,
                           f'Your subgroup: {found.subgroup}\nPlease choose subgroup:',
                           reply_markup=kb.chooseKeyboard)
