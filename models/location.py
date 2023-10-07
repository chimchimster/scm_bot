from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(75))

    __table_args__ = (
        UniqueConstraint('title', name='uq_title'),
    )

    location = relationship('Location', back_populates='city')
    item = relationship('ItemCityAssociation', back_populates='city')


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))

    city_id = Column(Integer, ForeignKey('cities.id'))

    __table_args__ = (
        UniqueConstraint('title', name='uq_title'),
    )

    city = relationship('City', back_populates='location')