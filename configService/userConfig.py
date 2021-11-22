from configService import registrationConfig
from configService.botConfig import bot


async def changeGroup(callback_query):
    if callback_query.data == 'group1':
        await registrationConfig.saveUser(callback_query, 1)
        await bot.send_message(callback_query.from_user.id, 'Subgroup 1 saved!')

    elif callback_query.data == 'group2':
        await registrationConfig.saveUser(callback_query, 2)
        await bot.send_message(callback_query.from_user.id, 'Subgroup 2 saved!')