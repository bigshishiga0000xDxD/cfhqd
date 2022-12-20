from typing import Iterable
from sqlalchemy import select

from cfhqd.db import session, WatchedUser, Chat, User


async def delete_chat(chat_id: int):
    async with session.begin():
        chat = await session.get(Chat, chat_id)
        if chat is not None:
            await session.delete(chat)


async def delete_users(chat_id: int, args: Iterable[str]):
    async with session.begin():
        users = set(map(lambda x: x.lower(), args))

        stmt = select(WatchedUser).where(WatchedUser.chat_id == chat_id)
        watched_users = (await session.execute(stmt)).scalars()

        stmt = select(WatchedUser.user_id).where(WatchedUser.chat_id == chat_id)
        stmt = select(User).where(User.user_id.in_(stmt))
        users = (await session.execute(stmt)).scalars()
        users = {user.user_id: user.handle for user in users}

        for user in watched_users:
            if users[user.user_id] in args:
                await session.delete(user)

