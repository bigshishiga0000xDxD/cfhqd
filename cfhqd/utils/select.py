from sqlalchemy import select

from cfhqd.db import session, Keys, User, WatchedUser, Contest, Chat
from cfhqd.models import UserModel, KeysModel, ContestModel

async def select_keys(chat_id: int):
    async with session.begin():
        keys = await session.get(Keys, chat_id)
        if keys is None:
            return None
        else:
            return KeysModel(open=keys.open, secret=keys.secret)

async def select_users(chat_id: int):
    async with session.begin():
        stmt = select(WatchedUser.user_id).where(WatchedUser.chat_id == chat_id).subquery()
        stmt = select(User).where(User.user_id.in_(stmt))

        users = (await session.execute(stmt)).scalars()

        return [
            UserModel(handle=user.handle, handle_cf=user.handle_cf)
            for user in users
        ]

async def select_contests():
    async with session.begin():
        contests = (await session.execute(select(Contest))).scalars()
        return {contest.contest_id for contest in contests}


async def select_chats():
    async with session.begin():
        chats = (await session.execute(select(Chat))).scalars()
        return [chat.chat_id for chat in chats]

