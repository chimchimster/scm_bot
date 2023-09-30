from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from database import *


class AuthenticateUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        telegram_id = event.from_user.id
        telegram_name = event.from_user.username

        user = await create_user(telegram_id, telegram_name)

        if user == Signal.USER_EXISTS:
            is_authenticated = await user_is_authenticated(telegram_id)

            if is_authenticated:
                data['state'] = 'available_for_purchases'
            else:
                data['state'] = 'waiting_for_authentication'

        else:
            data['state'] = 'waiting_for_registration'

        return await handler(event, data)
