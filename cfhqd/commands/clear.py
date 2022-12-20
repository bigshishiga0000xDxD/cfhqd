from aiogram import types

from cfhqd.utils import delete_chat

async def clear(message: types.Message):
    chat_id = message.chat.id

    await delete_chat(chat_id)
    
    await message.bot.send_message(
        message.chat.id,
        'Успех!'
    )
