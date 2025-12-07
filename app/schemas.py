import hashlib
from datetime import datetime
from enum import Enum

from loguru import logger
from pydantic import BaseModel, Field

from app.config import link_template, salt
from app.crypto import decrypt_data, encrypt_data


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

    def value_id(self) -> int:
        if self == Building.POKROVKA:
            return 1
        elif self == Building.MYASO:
            return 2
        elif self == Building.BASMAN:
            return 3
        return -1

    @classmethod
    def from_value_id(cls, value: int):
        if value == 1:
            return cls.POKROVKA
        elif value == 2:
            return cls.MYASO
        elif value == 3:
            return cls.BASMAN
        raise ValueError(f"Invalid building value: {value}")


class Mail(BaseModel):
    number: int = 0  # номер письма
    sender: str = None  # телеграм id отправителя
    send_building: Building = None  # строение отправки
    recipient_name: str = None  # ФИО получателя
    recipient_email: str = None  # корпоративная почта получателя
    timestamp: datetime = None  # время отправки

    def generate_number(self, counter: int, salt: str = salt) -> int:
        prime = 999983
        salt_hash = int(hashlib.sha256(salt.encode()).hexdigest()[:8], 16)
        magic = (salt_hash % (prime - 1)) + 1

        # Биективное преобразование
        number = (counter * magic) % prime

        # Дополнительная непредсказуемость через XOR (тоже биективно)
        xor_key = (
            int(hashlib.sha256(f"{salt}_xor".encode()).hexdigest()[:8], 16) % 1000000
        )
        number = number ^ xor_key

        return f"{number:06d}"

    @staticmethod
    def get_counter_from_number(number: str, salt: str = salt) -> int:
        """
        Обратное преобразование: из номера получаем counter.

        Args:
            number: Шестизначный номер (строка)
            salt: Соль (должна совпадать с той, что использовалась при генерации)

        Returns:
            counter - порядковый номер письма
        """
        prime = 999983
        number_int = int(number)

        # Шаг 1: Убираем XOR (XOR обратим сам по себе)
        xor_key = (
            int(hashlib.sha256(f"{salt}_xor".encode()).hexdigest()[:8], 16) % 1000000
        )
        number_int = number_int ^ xor_key

        # Шаг 2: Вычисляем модульное обратное к magic
        salt_hash = int(hashlib.sha256(salt.encode()).hexdigest()[:8], 16)
        magic = (salt_hash % (prime - 1)) + 1
        magic_inverse = pow(magic, -1, prime)  # Модульное обратное

        # Шаг 3: Обратное преобразование
        counter = (number_int * magic_inverse) % prime

        return counter


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
    decrypted_data = decrypt_data(encrypted_data)
    parts = decrypted_data.split("_")
    return LinkType(parts[0]), int(parts[1])
