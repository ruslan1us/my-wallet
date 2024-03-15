from datetime import datetime, timezone
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from src.base_maker import Base


class Salary(Base):
    __tablename__ = 'salary'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float]
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Tip(Base):
    __tablename__ = 'tip'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
