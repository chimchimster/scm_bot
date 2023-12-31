from sqlalchemy import Column, Integer, ForeignKey, String, Text, LargeBinary, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base
from .location import City


class ItemCityAssociation(Base):

    __tablename__ = 'item_city'

    id = Column(Integer, primary_key=True, autoincrement=True)

    item_id = Column(Integer, ForeignKey('item.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))

    item = relationship('Item', back_populates='city')
    city = relationship('City', back_populates='item')


class ItemCategoryAssociation(Base):

    __tablename__ = 'item_category'

    id = Column(Integer, primary_key=True, autoincrement=True)

    category_id = Column(Integer, ForeignKey('categories.id'))
    item_id = Column(Integer, ForeignKey('item.id'))

    item = relationship('Item', back_populates='category')
    category = relationship('Category', back_populates='item')


class Item(Base):

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(LargeBinary, nullable=True)
    price = Column(Numeric, default=0.0)
    quantity = Column(Integer, default=0)

    category = relationship('ItemCategoryAssociation', back_populates='item')
    order = relationship('Order', back_populates='item')
    city = relationship('ItemCityAssociation', back_populates='item')

    __table_args__ = (
        UniqueConstraint('title', name='uq_item_title'),
    )


class Category(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=10), nullable=False)

    item = relationship('ItemCategoryAssociation', back_populates='category')

    __table_args__ = (
        UniqueConstraint('title', name='uq_cat_title'),
    )
