'''
Расписание с фильтрацией и возможность зарегистироваться:
- Просмотр всей проги
- На определённый день
- В определённом корпусе
Регистрация по определённой ссылке для пиара, складывать в табличку
'''

from pydantic import BaseModel

bot_username = "event_bot"

class Event(BaseModel):
    id: str
    name: str
    date: str
    building: str

    def link(self) -> str:
        return f"https://t.me/{bot_username}?start=event_id{self.id}"

def get_events(date: str | None = None, building: str | None = None) -> list[Event]:
    # Функция для получения событий на определённый день и корпус, если нет параметров, то возвращает все события
    pass

def register_event(event_id: str) -> bool:
    # Функция для регистрации пользователя на событие
    pass
