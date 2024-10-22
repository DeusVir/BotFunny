import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from Handlers import usual_commands
from Handlers.introduction import  introduction
from admin import add_meme, add_anecdote, add_riddle

from database import database
#from aiogram.fsm.storage.redis import RedisStorage
from Handlers.entertainments import memes, anecdotes, riddle, horoscope
import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

API_TOKEN = os.getenv("API_TOKEN")

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=API_TOKEN)


async def main():
    #storage: RedisStorage = RedisStorage.from_url('redis://localhost')
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    dp.include_router(usual_commands.router)
    dp.include_router(introduction.router)
    dp.include_router(add_meme.router)
    dp.include_router(memes.router)
    dp.include_router(add_anecdote.router)
    dp.include_router(anecdotes.router)
    dp.include_router(add_riddle.router)
    dp.include_router(riddle.router)
    dp.include_router(horoscope.router)
    database.sql_start()
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
