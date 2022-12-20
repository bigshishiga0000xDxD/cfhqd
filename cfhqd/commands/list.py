from aiogram import types

from cfhqd.utils import select_users

async def list(message: types.Message):
    users = await select_users(message.chat.id)
    resp = '\n'.join(map(lambda x: x.handle_cf, users))

    await message.bot.send_message(
        message.chat.id,
        f'`{resp}`' if resp else 'Пусто!',
        parse_mode='markdown'
    )

