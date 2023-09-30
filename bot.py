import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_reader import bot_config


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=bot_config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())