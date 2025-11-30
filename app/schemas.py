from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.config import link_template
from app.crypto import decrypt_data, encrypt_data


class LinkType(Enum):
    EVENT = "event"
    USER = "user"


class MyBaseModel(BaseModel):
    link_type: LinkType

    def link(self) -> str:
        return link_template.format(
            encrypted=encrypt_data(f"{self.link_type.value}_{self.id}")
        )


class Mark(BaseModel):
    id: int
    sender: str  # телеграм id отправителя
    timestamp: str  # время отправки
    status: str  # статус отметки


class Mail(BaseModel):
    id: int
    sender: str  # телеграм id отправителя
    recipient: str  # телеграм id получателя
    timestamp: str  # время отправки
    status: str  # статус письма


class Building(Enum):
    POKROVKA = "Покровский бульвар, 11"
    MYASO = "Мясницкая, 20"
    BASMAN = "Старая Басманная улица, 21/4"


class Event(MyBaseModel):
    id: int  # id события
    name: str  # название события
    date: datetime  # дата события
    building: Building  # корпус события
    link_type: LinkType = LinkType.EVENT


class User(MyBaseModel):
    id: int  # id пользователя
    name: str  # имя пользователя
    email: str  # email пользователя
    phone: str  # телефон пользователя
    events: list[Event] = Field(default_factory=list)  # события пользователя
    marks: list[Mark] = Field(default_factory=list)  # отметки пользователя
    mails: list[Mail] = Field(default_factory=list)  # письма пользователя
    link_type: LinkType = LinkType.USER


def typed_decrypt_data(encrypted_data: str) -> tuple[LinkType, int]:
    decrypted_data = decrypt_data(encrypted_data).split("_")
    return LinkType(decrypted_data[0]), int(decrypted_data[1])
