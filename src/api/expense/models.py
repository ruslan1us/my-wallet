from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base_maker import Base

from src.api.time_func import set_date


class MoneySpinnerTable(Base):
    __tablename__ = 'money_spinner'
    __table_args__ = (
        UniqueConstraint('name', 'owner_id', name='uq_moneyspinner_name_owner'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    expenses: Mapped[list["Expense"]] = relationship("Expense")


class Expense(Base):
    __tablename__ = 'expense'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str | None]
    expensed_at: Mapped[datetime] = mapped_column(default=set_date)
    expense_place: Mapped[int] = mapped_column(ForeignKey('money_spinner.id'))
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__ = (
        UniqueConstraint('name', 'owner_id', name='uq_subscription_name_owner'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
