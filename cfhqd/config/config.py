from os import environ
from pydantic import BaseSettings

class Settings(BaseSettings):
    TOKEN = environ.get('TOKEN', '')

    DB_HOST = environ.get('DB_HOST', 'localhost')
    DB_USERNAME = environ.get('DB_USERNAME', 'postgres')
    DB_NAME = environ.get('DB_NAME', 'cfhqd')
    DB_PASSWORD = environ.get('DB_PASSWORD', 'postgres')
    DB_PORT = environ.get('DB_PORT', 5432)

    CONTESTS_CHECKED = 10
    CHECK_INTERVAL = 60

    @property
    def db_uri(self):
        return 'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'.format(**self.__dict__)


