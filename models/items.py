from sqlalchemy import Column, Integer, ForeignKey, String, Text, LargeBinary, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base
from .location import City


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(LargeBinary, nullable=True)
    price = Column(Numeric, default=0.0)
    quantity = Column(Integer, default=0)
    city_id = Column(Integer, ForeignKey('cities.id'))

    category = relationship('Category', back_populates='item')
    order = relationship('Order', back_populates='item')

    __table_args__ = (
        UniqueConstraint('title', name='uq_item_title'),
    )


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=10), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'))

    item = relationship('Item', back_populates='category')

    __table_args__ = (
        UniqueConstraint('title', name='uq_cat_title'),
    )