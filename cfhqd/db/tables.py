import uuid

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, UUID

from cfhqd.models import UserModel

def gen_uuid():
    return str(uuid.uuid4())

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID, primary_key=True, default=gen_uuid) 
    handle = Column(TEXT, nullable=False, unique=True)
    handle_cf = Column(TEXT, nullable=False)

    @staticmethod
    def create_row(user: UserModel) -> dict:
        return {
            'handle': user.handle,
            'handle_cf': user.handle_cf
        }

class Chat(Base):
    __tablename__ = 'chats'

    chat_id = Column(INTEGER, primary_key=True)

    users = relationship('WatchedUser', cascade='all,delete', backref='chats')
    keys = relationship('Keys', cascade='all,delete', backref='chats')

class WatchedUser(Base):
    __tablename__ = 'watched_users'

    row_id = Column(UUID, primary_key=True, default=gen_uuid)
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    chat_id = Column(ForeignKey('chats.chat_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'chat_id'),
    )

    @staticmethod
    def create_row(user_id, chat_id):
        return {
            'user_id': user_id,
            'chat_id': chat_id
        }

class Keys(Base):
    __tablename__ = 'keys'

    chat_id = Column(ForeignKey('chats.chat_id'), primary_key=True)
    open = Column(TEXT, nullable=False)
    secret = Column(TEXT, nullable=False)

class Contest(Base):
    __tablename__ = 'contests'

    contest_id = Column(INTEGER, primary_key=True)

