"""
Логика работы с письмами
"""

from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from loguru import logger

from app.schemas import Building, Mail


class MailStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()


async def save_mail_to_db(mail: Mail) -> tuple[int, int]:
    from app.database import MailDB, get_session

    session = get_session()
    try:
        mail_db = MailDB(
            number=0,
            sender=int(mail.sender),
            send_building=mail.send_building.value_id(),
            recipient_name=mail.recipient_name,
            recipient_email=mail.recipient_email,
            timestamp=mail.timestamp,
        )
        session.add(mail_db)
        session.commit()
        session.refresh(mail_db)

        number = mail.generate_number(mail_db.id)
        mail_db.number = number
        session.commit()

        return mail_db.id, number
    except Exception as e:
        logger.error(f"Ошибка при сохранении письма: {e}")
        session.rollback()
        return 0, 0
    finally:
        session.close()


async def answer_mail(building: Building, message: Message, state: FSMContext) -> None:
    await state.update_data(building=building, sender=str(message.from_user.id))
    await state.set_state(MailStates.waiting_for_name)
    await message.answer(
        "Привет! Для отправки пиьсма необходимо заполнить несколько полей.\n"
        f"Корпус отправки: {building.value}\n\n"
        "Введите ФИО получателя"
    )


async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(recipient_name=message.text)
    await state.set_state(MailStates.waiting_for_email)
    await message.answer("Введите корпоративную почту получателя (@edu.hse.ru)")


async def process_email(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.endswith("@edu.hse.ru"):
        await message.answer(
            "Введите корректную корпоративную почту получателя в формате @edu.hse.ru"
        )
        return

    data = await state.get_data()
    confirm_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data="mail_confirm")],
            [InlineKeyboardButton(text="Отменить", callback_data="mail_cancel")],
        ]
    )
    await message.answer(
        f"Проверьте данные:\n"
        f"ФИО получателя: {data['recipient_name']}\n"
        f"Почта: {message.text}",
        reply_markup=confirm_keyboard,
    )
    await state.update_data(recipient_email=message.text)


async def confirm_mail(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    mail = Mail(
        sender=data["sender"],
        send_building=data["building"],
        recipient_name=data["recipient_name"],
        recipient_email=data["recipient_email"],
        timestamp=datetime.now(),
    )

    mail_id, mail_number = await save_mail_to_db(mail)
    if not mail_id:
        logger.error(f"Произошла ошибка при сохранении письма в БД: {mail}")
        await callback.message.edit_text("Произошла ошибка при сохранении письма")
        return

    await callback.message.edit_text(
        f"Письмо создано!\n"
        f"Для отправки напишите номер письма на конверте и положите его в почтовый ящик.\n"
        f"Номер письма: {mail_number}\n"
    )
    await state.clear()
    await callback.answer()


async def cancel_mail(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text("Отправка отменена")
    await state.clear()
    await callback.answer()


# def generate_stamp():
#     # сохранить в БД данные по заявке
#     # mail: Mail = save_to_db(mail)
#     # number = mail.generate_number(mail.id, counter)

#     # Создать
#     mail = Mail(
#         sender="1234567890",
#         send_building=Building.POKROVKA,
#         recipient_email="rksinitsyn@edu.hse.ru",
#         timestamp=datetime.now(),
#     )
#     id = 3  # TODO: из БД
#     mail.number = mail.generate_number(id)

#     return mail.generate_number(id)


# корпортивная почта (кому)
# получение номера ""
# отправка номера в письме
