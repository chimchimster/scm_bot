from aiogram.filters.callback_data import CallbackData


class CityCallback(CallbackData, prefix='city'):
    id: int
    title: str


class LocationCallback(CallbackData, prefix='location'):
    id: int
    title: str


class ItemCallback(CallbackData, prefix='item'):
    id: int
    title: str


class CategoryCallback(CallbackData, prefix='category'):
    id: int
    title: str
