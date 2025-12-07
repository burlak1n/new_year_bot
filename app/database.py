from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite:///mail.db")


class Base(DeclarativeBase):
    pass


class MailDB(Base):
    __tablename__ = "mails"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(nullable=False)
    sender: Mapped[int] = mapped_column(nullable=False)
    send_building: Mapped[int] = mapped_column(nullable=False)
    recipient_name: Mapped[str] = mapped_column(nullable=False)
    recipient_email: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)


Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
