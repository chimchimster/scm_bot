from aiogram.filters.callback_data import CallbackData


class CityCallback(CallbackData, prefix='city'):
    id: int
    title: str
    callback_name: str = 'city'


class LocationCallback(CallbackData, prefix='location'):
    id: int
    title: str
    callback_name: str = 'city'


class ItemCallback(CallbackData, prefix='item'):
    id: int
    title: str
    callback_name: str = 'item'


class CategoryCallback(CallbackData, prefix='category'):
    id: int
    title: str
    callback_data: str = 'category'

