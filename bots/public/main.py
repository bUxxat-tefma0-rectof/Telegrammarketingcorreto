import asyncio
from aiogram import Bot, Dispatcher
from config.settings import settings
from bots.public.handlers import setup_public_handlers

bot = Bot(token=settings.TELEGRAM_PUBLIC_TOKEN, parse_mode="HTML")
dp = Dispatcher()

setup_public_handlers(dp)

async def main():
    print("🤖 Bot Público iniciado...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
