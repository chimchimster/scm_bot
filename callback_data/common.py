from aiogram.filters.callback_data import CallbackData


class CityCallback(CallbackData, prefix='city'):
    id: int
    title: str
    callback_name: str = 'city'


class LocationCallback(CallbackData, prefix='location'):
    id: int
    title: str
    callback_name: str = 'city'

