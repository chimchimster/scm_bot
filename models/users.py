import time

from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Text, Numeric, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


Base = DeclarativeBase()


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

    auth_key = Column(Text, nullable=False)
    expired_at_unix = Column(BigInteger, default=int(time.time()))
    expired = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='session')


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(LargeBinary, nullable=True)
    price = Column(Numeric, default=0.0)

    category = relationship('Category', back_populates='item')


class Category(Base):
    __tablename__ = 'categories'

    title = Column(String(length=10), nullable=False)

    item_id = Column(Integer, ForeignKey('item.id'))

    item = relationship('Item', back_populates='categories')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(BigInteger)
    expired_at = Column(BigInteger)
    expired = Column(Boolean, default=False)
    paid = Column(Boolean, default=False)

    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', back_populates='orders')

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='orders')