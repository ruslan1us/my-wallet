from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base_maker import Base

from src.api.time_func import set_date


class MoneySpinnerTable(Base):
    __tablename__ = 'money_spinner'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    expenses: Mapped[list["Expense"]] = relationship("Expense")


class Expense(Base):
    __tablename__ = 'expense'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float]
    description: Mapped[str | None]
    expensed_at: Mapped[datetime] = mapped_column(default=set_date)
    expense_place: Mapped[int] = mapped_column(ForeignKey('money_spinner.id'))
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class Subscription(Base):
    __tablename__ = 'subscription'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
