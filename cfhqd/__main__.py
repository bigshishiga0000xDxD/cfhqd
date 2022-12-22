from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_polling
from aiohttp import ClientError

import logging
import asyncio

from cfhqd.commands import start, help, add, add_keys, clear, list, ratings, remove, sync
from cfhqd.config import settings
from cfhqd.requests import check_changes, APIException
from cfhqd.utils import aggregate_changes
from cfhqd.db import init_tables


def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(settings.TOKEN)
    dispatcher = Dispatcher(bot)

    dispatcher.register_message_handler(callback=start, commands=['start'])
    dispatcher.register_message_handler(callback=help, commands=['help'])
    dispatcher.register_message_handler(callback=add, commands=['add'])
    dispatcher.register_message_handler(callback=add_keys, commands=['addkeys'])
    dispatcher.register_message_handler(callback=clear, commands=['clear'])
    dispatcher.register_message_handler(callback=list, commands=['list'])
    dispatcher.register_message_handler(callback=ratings, commands=['ratings'])
    dispatcher.register_message_handler(callback=remove, commands=['remove'])
    dispatcher.register_message_handler(callback=sync, commands=['sync'])

    async def watch_changes(dispatcher):
        while True:
            try:
                contest = await check_changes()
                messages = await aggregate_changes(contest)

                for message in messages:
                    await dispatcher.bot.send_message(
                        message.chat_id,
                        message.text,
                        parse_mode='markdown'
                    )

                if messages:
                    continue
            except ClientError as e:
                logging.critical(str(e))
            except APIException as e:
                logging.critical(str(e))

            await asyncio.sleep(settings.CHECK_INTERVAL)

    async def on_startup(dispatcher):
        await init_tables()
        asyncio.create_task(watch_changes(dispatcher))

    start_polling(dispatcher, on_startup=on_startup)

if __name__ == '__main__':
    main()
