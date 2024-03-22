from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from src.base_maker import Base
from sqlalchemy import ForeignKey

from src.api.time_func import set_date


class Salary(Base):
    __tablename__ = 'salary'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float]
    date: Mapped[datetime] = mapped_column(default=set_date)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))


class Tip(Base):
    __tablename__ = 'tip'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    date: Mapped[datetime] = mapped_column(default=set_date)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))

