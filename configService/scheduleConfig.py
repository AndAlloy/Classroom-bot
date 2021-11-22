from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State

from configService import botConfig
from model.base import Session
from model.lesson import Lesson
from model.user import User


class Lessons(StatesGroup):
    name = State()
    startTime = State()
    endTime = State()
    teacher = State()
    place = State()
    subgroup = State()
    day = State()


async def getSchedule(callback_query):
    session = Session()
    newUser = User(callback_query)
    found = session.query(User) \
        .filter(User.telegramId == newUser.telegramId) \
        .first()
    lessons = session.query(Lesson) \
        .filter(Lesson.subgroup == found.subgroup) \
        .all()
    message = ''

    index = 1
    for lesson in lessons:
        message += f'{index}. ({str(lesson.startTime)[:5]} -> {str(lesson.endTime)[:5]}, ' \
                   f'{lesson.day})\nName: {lesson.name}, Teacher: {lesson.teacher}\n'
        index = index + 1
    await botConfig.bot.send_message(callback_query.from_user.id, message)


async def inputSchedule(callback_query):
    await types.ChatActions.typing()
    await botConfig.bot.send_message(callback_query.from_user.id,
                                     'Here you can add lesson to schedule.\n'
                                     'At first, type the name of the lesson')
    await Lessons.name.set()


async def getName(callback_query, state):
    async with state.proxy() as data:
        data['name'] = callback_query.text
    await botConfig.bot.send_message(callback_query.from_user.id, 'Send start time (HH:mm)')
    await Lessons.startTime.set()


async def getStartTime(callback_query, state):
    async with state.proxy() as data:
        data['startTime'] = callback_query.text
    await botConfig.bot.send_message(callback_query.from_user.id, 'Send end time (HH:mm)')
    await Lessons.endTime.set()


async def getEndTime(callback_query, state):
    async with state.proxy() as data:
        data['endTime'] = callback_query.text
    await botConfig.bot.send_message(callback_query.from_user.id, 'Send place')
    await Lessons.place.set()


async def getPlace(callback_query, state):
    async with state.proxy() as data:
        data['place'] = callback_query.text
    await botConfig.bot.send_message(callback_query.from_user.id, 'Send teacher')
    await Lessons.teacher.set()


async def getTeacher(callback_query, state):
    async with state.proxy() as data:
        data['teacher'] = callback_query.text
    await botConfig.bot.send_message(callback_query.from_user.id, 'Send subgroup')
    await Lessons.subgroup.set()


async def getSubgroup(callback_query, state):
    async with state.proxy() as data:
        data['subgroup'] = callback_query.text
    await botConfig.bot.send_message(callback_query.from_user.id, 'Send day')
    await Lessons.day.set()


async def getDay(callback_query, state):
    async with state.proxy() as data:
        data['day'] = callback_query.text
    try:
        await saveLesson(data)
        await botConfig.bot.send_message(callback_query.from_user.id, 'Saved')
    except Exception as e:
        await botConfig.bot.send_message(callback_query.from_user.id, 'Error: ' + str(e))
    await state.finish()


async def saveLesson(data):
    await types.ChatActions.typing()
    newLesson = Lesson(
        data['name'],
        datetime.strptime(data['startTime'], '%H:%M').time(),
        datetime.strptime(data['endTime'], '%H:%M').time(),
        data['teacher'],
        data['place'],
        int(data['subgroup']),
        data['day']
    )
    session = Session()
    session.add(newLesson)
    session.commit()
    session.close()
