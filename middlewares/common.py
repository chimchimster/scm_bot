from typing import Union
from aiogram.types import Message

from database import *
from states import *


async def get_auth_state(message: Message) -> Union[AuthenticationState, None]:
    telegram_id = message.from_user.id

    has_user = await user_exists(telegram_id)

    if has_user == Signal.USER_EXISTS:

        is_banned = await user_is_banned(telegram_id)

        if is_banned == Signal.USER_IS_BANNED:
            await message.answer(text='Вы заблокированы!')
            return

        is_restricted = await user_is_restricted(telegram_id)

        if is_restricted == Signal.USER_IS_RESTRICTED:
            await message.answer(text='Вы временно заблокированы!')
            return

        is_authenticated = await user_is_authenticated(telegram_id)

        if is_authenticated == Signal.USER_AUTHORIZED:
            return AuthenticationState.available_for_purchases
        else:
            return AuthenticationState.waiting_for_authentication
    else:
        return AuthenticationState.waiting_for_registration
