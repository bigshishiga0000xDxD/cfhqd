from aiogram import types

from cfhqd.utils import insert_keys, insert_chat

async def add_keys(message: types.Message):
    args = message.text.split()[1:]

    if len(args) != 2:
        await message.bot.send_message(
            message.chat.id,
            'Неправильный синтаксис: надо ввести окрытый и закрытый ключ (через пробел)'
        )
        return
    else:
        open, secret = args

        await insert_chat(message.chat.id)
        await insert_keys(message.chat.id, open, secret)
        
        await message.bot.send_message(
            message.chat.id,
            'Успех!'
        )
