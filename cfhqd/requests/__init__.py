import aiohttp

from .cf import get_users, get_friends, check_changes, APIException

http_session = aiohttp.ClientSession()
base_url = 'https://codeforces.com/api'

