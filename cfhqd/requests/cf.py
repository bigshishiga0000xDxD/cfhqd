from typing import Optional
import logging

import cfhqd.requests as common
from cfhqd.models import UserModel, ContestModel, RatingChangeModel
from cfhqd.config import settings
from cfhqd.utils import select_contests
from .auth import make_query


class APIException(Exception):
    def __init__(self, message):
        super().__init__(message)

class RatingsUnavailableException(APIException):
    def __init__(self, message):
        super().__init__(message)


async def read_and_load(url: str, params=None) -> dict:
    async with common.http_session.get(url, params=params) as resp:
        json = await resp.json()

        if json['status'] == 'OK':
            return json['result']
        else:
            if json['comment'] == 'contestId: Rating changes are unavailable for this contest':
                raise RatingsUnavailableException('')
            else:
                raise APIException(json['comment'])

async def get_users(users: list[UserModel]) -> list[UserModel]:
    handles = [user.handle for user in users]
    url = f'{common.base_url}/user.info?handles=' + ';'.join(handles)

    json = await read_and_load(url)

    return [
        UserModel(
            handle=user['handle'].lower(),
            handle_cf=user['handle'],
            rating=user.get('rating')
        )
        for user in json
    ]

async def get_friends(open: str, secret: str):
    url = make_query({'onlyOnline': 'false'}, 'user.friends', open, secret)
    json = await read_and_load(url)

    return [
        UserModel(
            handle=handle.lower(),
            handle_cf=handle
        )
        for handle in json
    ]

async def check_changes() -> Optional[ContestModel]:
    candidates = set()
    json = await read_and_load(f'{common.base_url}/contest.list')

    i = -1
    while True:
        i += 1
        if json[i]['phase'] != 'FINISHED':
            continue
        
        candidates.add(json[i]['id']) 
        if len(candidates) == settings.CONTESTS_CHECKED:
            break

    updated = candidates - (await select_contests())
    logging.info(updated)

    for contest_id in updated:
        try:
            json = await read_and_load(
                f'{common.base_url}/contest.ratingChanges',
                params={'contestId': contest_id}
            )
        except RatingsUnavailableException:
            continue

        return ContestModel(
            id=contest_id,
            name=json[0]['contestName'],
            result=[
                RatingChangeModel(
                    handle = change['handle'],
                    oldRating = change['oldRating'],
                    newRating = change['newRating']
                )
                for change in json
            ]
        )
