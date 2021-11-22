from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

changeButton = InlineKeyboardButton('Change group', callback_data='change_group')
addSchedule = InlineKeyboardButton('Schedule: add lesson', callback_data='add_lesson')
showSchedule = InlineKeyboardButton('Show schedule', callback_data='show_schedule')
menuKeyboard = InlineKeyboardMarkup(row_width=2).add(changeButton, addSchedule, showSchedule)

groupButton1 = InlineKeyboardButton('1', callback_data='group1')
groupButton2 = InlineKeyboardButton('2', callback_data='group2')
chooseKeyboard = InlineKeyboardMarkup(row_width=2).add(groupButton1, groupButton2)


