from datetime import datetime

from sqlalchemy import Column, TIMESTAMP,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


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
    expensed_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    expense_place: Mapped[int] = mapped_column(ForeignKey('money_spinner.id'))

