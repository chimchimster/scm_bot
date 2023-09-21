import asyncio

from dispatch import dp, bot
from handlers.user import menu_router


dp.include_router(menu_router)


async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())