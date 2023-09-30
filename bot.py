import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import bot_config
from handlers.authentication import router as auth_router
from middlewares.authentication import AuthenticateUserMiddleware


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=bot_config.bot_token.get_secret_value(), parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.outer_middleware(AuthenticateUserMiddleware())
    dp.include_router(auth_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())