from os import environ
from pydantic import BaseSettings

class Settings(BaseSettings):
    TOKEN = environ.get('TOKEN', '')

    DB_NAME = environ.get('DB_NAME', 'cfhqd')
    POSTGRES_USER = environ.get('DB_USERNAME', 'postgres')
    POSTGRES_PASSWORD = environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = environ.get('DB_HOST', 'localhost')
    DB_PORT = environ.get('DB_PORT', 5432)

    CONTESTS_CHECKED = 10
    CHECK_INTERVAL = 60

    @property
    def db_uri(self):
        return 'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'.format(**self.__dict__)


