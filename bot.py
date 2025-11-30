import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.events import answer_event
from app.user import answer_user
from app.schemas import LinkType, typed_decrypt_data
from loguru import logger
from app.config import BOT_TOKEN
import logging

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) > 1:
        encrypted = args[1]
        try:
            link_type, entity_id = typed_decrypt_data(encrypted)
            if link_type == LinkType.EVENT:
                await answer_event(entity_id, message)
            elif link_type == LinkType.USER:
                await answer_user(entity_id, message)
        except Exception as e:
            logger.error(f"Произошла ошибка при обработке ссылки: {e}")
            await message.answer("Произошла ошибка при обработке ссылки. Пожалуйста, обратитесь к @burlak1n")
    else:
        await message.answer("Hello, world!")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
