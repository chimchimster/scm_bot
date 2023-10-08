from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from .common import get_auth_state


class AuthenticateUserMessageMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ):

        auth_state = await get_auth_state(message)

        if auth_state:

            data['auth_state'] = auth_state

            return await handler(message, data)

