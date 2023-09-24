from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self._chat_type = chat_type

    async def __call__(self, message: Message):
        if isinstance(message.chat.type, str):
            return self._chat_type == message.chat.type
        else:
            return message.chat.type in self._chat_type