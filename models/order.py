from sqlalchemy import Column, BigInteger, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


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