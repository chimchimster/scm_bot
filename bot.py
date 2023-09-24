import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import group_names, usernames, checkin, ordering_food, common

from config_reader import config
from middlewares.weekend import WeekendCallbackMiddleware

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()
    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())
    dp.include_routers(common.router, group_names.router, usernames.router, checkin.router, ordering_food.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())