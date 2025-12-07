import hashlib
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.config import link_template, salt
from app.crypto import decrypt_data, encrypt_data
from loguru import logger


class LinkType(Enum):
    EVENT = "event"
    USER = "user"
    MAIL = "mail"


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


class Building(Enum):
    POKROVKA = "Покровский бульвар, 11"
    MYASO = "Мясницкая, 20"
    BASMAN = "Старая Басманная улица, 21/4"


class Mail(BaseModel):
    sender: str  # телеграм id отправителя
    send_building: Building  # строение отправки
    recipient: str  # корпоративная почта получателя
    timestamp: datetime  # время отправки

    def generate_number(self, mail_id: int, salt: str = salt):
        # counter - порядковый номер письма (можно из БД)
        # Но хешируем, чтобы не был предсказуемым
        hash_obj = hashlib.sha256(f"{mail_id}_{counter}_{salt}".encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        return f"{hash_int % 10000:04d}"


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
    logger.debug(f"Decrypting data: {encrypted_data}")
    decrypted_data = decrypt_data(encrypted_data).split("_")
    return LinkType(decrypted_data[0]), int(decrypted_data[1])
