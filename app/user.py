from aiogram.types import Message
from loguru import logger
from app import config
from app.schemas import User

def get_user(user_id: int) -> User:
    return User(id=user_id, name="John Doe", email="john.doe@example.com", phone="1234567890")

async def answer_user(user_id: int, message: Message) -> str:
    # TODO: Добавить получение пользователя
    logger.debug(f"Получение пользователя({user_id})")
    if message.from_user.id in config.ADMIN_IDS:
        # TODO: Добавить админ панель
        logger.debug(f"Админ{message.from_user.id} перешёл к пользователю с ID: {user_id}")
        await message.answer(f"Переход на пользователя({user_id})")
    elif message.from_user.id == user_id:
        # TODO: Добавить профиль
        logger.debug(f"{message.from_user.id} перешёл к своему профилю")
        await message.answer("Профиль")
    else:
        logger.debug(f"{message.from_user.id} перешёл к пользователю с ID: {user_id}")
        await message.answer("Hello, world!")