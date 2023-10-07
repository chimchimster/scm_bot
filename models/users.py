import time

from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(length=255), nullable=False)
    telegram_id = Column(BigInteger, nullable=False, index=True)
    is_blocked = Column(Boolean, default=False, nullable=False)
    is_restricted = Column(Boolean, default=False, nullable=False)

    session = relationship('Session', uselist=False, back_populates='user', cascade="all, delete-orphan")
    order = relationship('Order', back_populates='user', cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('telegram_id', name='uq_telegram_id'),
    )


class Session(Base):
    __tablename__ = 'session'

    auth_hash = Column(Text, nullable=False)
    created_at_unix = Column(BigInteger, default=int(time.time()), primary_key=True)
    expired = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='session')
