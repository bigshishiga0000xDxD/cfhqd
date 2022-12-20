import logging
from aiogram import types
from aiohttp import ClientError

from cfhqd.requests import get_friends, APIException
from cfhqd.utils import insert_users, insert_chat, select_keys

async def sync(message: types.Message):
    chat_id = message.chat.id

    await insert_chat(chat_id)
    keys = await select_keys(chat_id)

    if keys is None:
        await message.bot.send_message(
            chat_id,
            'Вы не ввели ключи! Выполните сначала /addkeys'
        )
        return

    try:
        users = await get_friends(keys.open, keys.secret)
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

    await insert_users(users, chat_id)

    await message.bot.send_message(
        chat_id,
        'Успех!'
    )

