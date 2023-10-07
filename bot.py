import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import bot_config
from handlers.authentication import router as auth_router
from handlers.navigation import router as nav_menu_router
from handlers.admin.panel import router as admin_router
from middlewares.authentication import *


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=bot_config.bot_token.get_secret_value(), parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.outer_middleware(AuthenticateUserMessageMiddleware())
    dp.message.outer_middleware(AuthenticateUserCallbackMiddleware())
    dp.include_routers(auth_router, admin_router, nav_menu_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())