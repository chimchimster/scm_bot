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

        has_user = await user_exists(telegram_id)

        if has_user == Signal.USER_EXISTS:

            is_banned = await user_is_banned(telegram_id)
            is_restricted = await user_is_restricted(telegram_id)

            if is_banned == Signal.USER_IS_BANNED:
                await event.answer(text='Вы заблокированы!')
                return
            if is_restricted == Signal.USER_IS_RESTRICTED:
                await event.answer(text='Вы временно заблокированы!')
                return

        await handler(event, data)
