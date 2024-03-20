from datetime import datetime, timezone

from sqlalchemy import Column, TIMESTAMP,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.base_maker import Base

from src.api.time_func import set_date


class MoneySpinnerTable(Base):
    __tablename__ = 'money_spinner'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Expense(Base):
    __tablename__ = 'expense'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float]
    description: Mapped[str | None]
    expensed_at: Mapped[datetime] = mapped_column(default=set_date)
    expense_place: Mapped[int] = mapped_column(ForeignKey('money_spinner.id'))

