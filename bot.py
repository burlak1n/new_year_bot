import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from app.config import BOT_TOKEN
from app.events import answer_event
from app.mail import (
    MailStates,
    answer_mail,
    cancel_mail,
    confirm_mail,
    process_email,
    process_name,
)
from app.schemas import Building, LinkType, typed_decrypt_data
from app.user import answer_user

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    args = message.text.split(maxsplit=1)

    if len(args) > 1:
        encrypted = args[1]
        try:
            link_type, entity_id = typed_decrypt_data(encrypted)
            if link_type == LinkType.EVENT:
                await answer_event(entity_id, message)
            elif link_type == LinkType.USER:
                await answer_user(entity_id, message)
            elif link_type == LinkType.MAIL:
                building = Building.from_value_id(entity_id)
                await answer_mail(building, message, state)
        except Exception as e:
            logger.error(f"Произошла ошибка при обработке ссылки: {e}")
            await message.answer(
                "Произошла ошибка при обработке ссылки. Пожалуйста, обратитесь к @burlak1n"
            )
    else:
        await message.answer("Hello, world!")


@dp.message(MailStates.waiting_for_name)
async def handle_name(message: Message, state: FSMContext):
    await process_name(message, state)


@dp.message(MailStates.waiting_for_email)
async def handle_email(message: Message, state: FSMContext):
    await process_email(message, state)


@dp.callback_query(lambda c: c.data == "mail_confirm")
async def handle_mail_confirm(callback: CallbackQuery, state: FSMContext):
    await confirm_mail(callback, state)


@dp.callback_query(lambda c: c.data == "mail_cancel")
async def handle_mail_cancel(callback: CallbackQuery, state: FSMContext):
    await cancel_mail(callback, state)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
