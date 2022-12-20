from aiogram import types


async def start(message: types.Message):
    await message.bot.send_message(
        message.chat.id,
        'Напишите /help чтобы узнать список команд'
    )
