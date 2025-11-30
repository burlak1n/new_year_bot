'''
Расписание с фильтрацией и возможность зарегистироваться:
- Просмотр всей проги
- На определённый день
- В определённом корпусе
Регистрация по определённой ссылке для пиара, складывать в табличку
'''

from datetime import datetime

from aiogram.types import Message
from app.schemas import Building, Event

def get_events(date: str | None = None, building: str | None = None) -> list[Event]:
    # Функция для получения событий на определённый день и корпус, если нет параметров, то возвращает все события
    pass

def get_event(event_id: int) -> Event:
    return Event(id=event_id, name="Event 1", date=datetime.now(), building=Building.POKROVKA)

def register_event(user_id: int, event_id: str) -> bool:
    pass

def unregister_event(user_id: int, event_id: str) -> bool:
    pass

def answer_event(event_id: int, message: Message) -> str:
    pass