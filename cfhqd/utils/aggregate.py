from collections import namedtuple

from cfhqd.models import MessageModel
from .select import select_chats, select_users
from .insert import insert_contest

RatingChange = namedtuple('RatingChange', ['handle', 'oldRating', 'newRating', 'delta'])

def string_delta(delta: int) -> str:
    if delta > 0:
        return f'+{delta}'
    else:
        return str(delta)

async def aggregate_changes(contest) -> list[MessageModel]:
    if contest is None:
        return []

    await insert_contest(contest.id)

    changes = {
        user_change.handle: (user_change.oldRating, user_change.newRating) 
        for user_change in contest.result
    }

    chats = await select_chats()
    result = []

    for chat_id in chats:
        users = await select_users(chat_id) 

        chat_changes = []
        for user in users:
            if user.handle_cf in changes.keys():
                chat_changes.append(RatingChange(
                    user.handle_cf,
                    changes[user.handle_cf][0],
                    changes[user.handle_cf][1],
                    changes[user.handle_cf][1] - changes[user.handle_cf][0]
                ))

        if not chat_changes:
            continue

        chat_changes.sort(key=lambda change: change.delta, reverse=True)
        longest_handle = max(map(lambda change: len(change.handle), chat_changes))

        message = f'{contest.name} был обновлен!\n\n'

        message += '`'
        message += '\n'.join(
            map(
                lambda change:
                f'{change.handle.ljust(longest_handle, " ")}   {change.oldRating} -> {change.newRating} ({string_delta(change.delta)})',
                chat_changes
            )
        )
        message += '`'

        result.append(MessageModel(
            chat_id=chat_id,
            text=message
        ))


    return result
