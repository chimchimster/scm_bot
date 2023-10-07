from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class CityLocationAssociation(Base):
    __tablename__ = 'city_location'

    id = Column(Integer, primary_key=True, autoincrement=True)

    city_id = Column(Integer, ForeignKey('cities.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    location = relationship('Location', back_populates='city')
    city = relationship('City', back_populates='location')


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(75))

    location = relationship('CityLocationAssociation', back_populates='city')
    item = relationship('ItemCityAssociation', back_populates='city')

    __table_args__ = (
        UniqueConstraint('title', name='uq_title'),
    )


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))

    city = relationship('CityLocationAssociation', back_populates='location')

    __table_args__ = (
        UniqueConstraint('title', name='uq_title'),
    )

