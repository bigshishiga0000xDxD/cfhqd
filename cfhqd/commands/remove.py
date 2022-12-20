from aiogram import types

from cfhqd.utils import delete_users

async def remove(message: types.Message):
    args = message.text.split()[1:]
    chat_id = message.chat.id

    if not args:
        await message.bot.send_message(
            chat_id,
            'Напишите хэндлы после команды'
        )
        return

    await delete_users(chat_id, args)
    
    await message.bot.send_message(
        chat_id,
        'Успех!'
    )

