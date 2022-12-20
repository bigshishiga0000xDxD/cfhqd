import logging
from aiogram import types
from aiohttp import ClientError

from cfhqd.models import UserModel
from cfhqd.requests import get_users, APIException
from cfhqd.utils import insert_users, insert_chat


async def add(message: types.Message):
    args = message.text.split()[1:]
    chat_id = message.chat.id

    if not args:
        await message.bot.send_message(
            chat_id,
            'Напишите хэндлы после команды'
        )
        return

    users = [UserModel(handle=handle) for handle in args]

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

    logging.info(f'commiting {users} to database')

    await insert_chat(chat_id)
    await insert_users(users, chat_id)
    
    await message.bot.send_message(
        message.chat.id,
        'Успех!'
    )
