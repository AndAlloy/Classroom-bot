from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from configService import registrationConfig, userConfig, botConfig, scheduleConfig, keyboardsConfig
from configService.botConfig import dp
from model.base import Base, engine

Base.metadata.create_all(engine)


class Lessons(StatesGroup):
    name = State()
    startTime = State()
    endTime = State()
    teacher = State()
    place = State()
    day = State()
    subgroup = State()


async def throttled(*args, **kwargs):
    message = args[0]


@dp.message_handler(content_types=['text'])
@dp.throttled(throttled, rate=0.5)
async def gg(message):
    reply = message.text
    if reply == '/start':
        await registrationConfig.start(message)
    elif reply == '/menu':
        await message.reply(f'Please choose option:', reply_markup=keyboardsConfig.menuKeyboard)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled input', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Lessons.all_states_names)
async def lessonsHandler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    if current_state == 'Lessons:name':
        await scheduleConfig.getName(message, state)
    elif current_state == 'Lessons:startTime':
        await scheduleConfig.getStartTime(message, state)
    elif current_state == 'Lessons:endTime':
        await scheduleConfig.getEndTime(message, state)
    elif current_state == 'Lessons:place':
        await scheduleConfig.getPlace(message, state)
    elif current_state == 'Lessons:teacher':
        await scheduleConfig.getTeacher(message, state)
    elif current_state == 'Lessons:subgroup':
        await scheduleConfig.getSubgroup(message, state)
    elif current_state == 'Lessons:day':
        await scheduleConfig.getDay(message, state)


@dp.callback_query_handler(lambda c: c.data in ['group1', 'group2'])
async def chooseSubgroup(callback_query):
    await userConfig.changeGroup(callback_query)


@dp.callback_query_handler(lambda c: c.data in ['change_group', 'add_lesson', 'show_schedule'])
async def menuHandler(callback_query: types.CallbackQuery):
    await botConfig.menuHandler(callback_query)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
