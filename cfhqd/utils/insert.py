from typing import Iterable
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from cfhqd.db import session, User, Chat, WatchedUser, Keys, Contest
from cfhqd.models import UserModel

async def insert_chat(chat_id: int):
    async with session.begin():
        stmt = insert(Chat).values([{'chat_id': chat_id}]).on_conflict_do_nothing()
        await session.execute(stmt)


async def insert_keys(chat_id: int, open: str, secret: str):
    async with session.begin():
        keys = await session.get(Keys, chat_id)
        if keys is not None:
            await session.delete(keys)

        keys = Keys(chat_id=chat_id, open=open, secret=secret) 
        session.add(keys)


async def insert_users(users: Iterable[UserModel], chat_id: int):
    async with session.begin():
        users = [User.create_row(user) for user in users]
        stmt = insert(User).values(users)

        stmt = stmt.on_conflict_do_update(
            index_elements=[User.handle], set_=dict(handle=stmt.excluded.handle)
        ).returning(User.user_id)

        stmt = select(User.user_id).from_statement(stmt)

        user_ids = (await session.execute(stmt)).scalars()
        users = [WatchedUser.create_row(user_id, chat_id) for user_id in user_ids]

        stmt = insert(WatchedUser).values(users).on_conflict_do_nothing()
        await session.execute(stmt) 

async def insert_contest(contest_id: int):
    async with session.begin():
        contest = Contest(contest_id=contest_id)
        session.add(contest)
