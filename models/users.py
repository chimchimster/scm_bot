import time

from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship


from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(length=255), nullable=False)
    telegram_id = Column(BigInteger, nullable=False, index=True)
    is_blocked = Column(Boolean, default=False, nullable=False)
    is_restricted = Column(Boolean, default=False, nullable=False)

    session = relationship('Session', uselist=False, back_populates='user')


class Session(Base):
    __tablename__ = 'session'

    auth_hash = Column(Text, nullable=False)
    created_at_unix = Column(BigInteger, default=int(time.time()), primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='session')
