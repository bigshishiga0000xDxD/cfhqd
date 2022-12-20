import logging
from aiogram import types
from aiohttp import ClientError

from cfhqd.requests import get_users, APIException
from cfhqd.utils import select_users

async def ratings(message: types.Message):
    chat_id = message.chat.id
    users = await select_users(message.chat.id)

    if not users:
        await message.bot.send_message(
            chat_id,
            'Пусто!'
        )
        return

    try:
        users = await get_users(users)
    except APIException as e:
        await message.bot.send_message(
            chat_id,
            f'API Codeforces вернул ошибку `{e}`',
            parse_mode='markdown'
        )
        logging.error(f'api exception {e} occured')
        return
    except ClientError as e:
        await message.bot.send_message(
            chat_id,
            f'Произошла ошибка при подключении. Скорее всего, codeforces сейчас недоступен'
        )
        logging.critical(f'connection exception {e} occured')
        return

    users.sort(key=lambda x: x.rating if x.rating is not None else 0, reverse=True)
    longest_handle = max(map(lambda x: len(x.handle), users))

    result = '\n'.join(
        map(lambda x: f'{x.handle_cf.ljust(longest_handle, " ")}   {x.rating}', users)
    )

    await message.bot.send_message(
        message.chat.id,
        f'`{result}`',
        parse_mode='markdown'
    )

