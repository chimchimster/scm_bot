import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import questions, different_types

from config_reader import config


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(questions.router, different_types.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())