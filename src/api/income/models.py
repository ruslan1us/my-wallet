from datetime import datetime
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Salary(Base):
    __tablename__ = 'salary'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[float]
    date = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class Tip(Base):
    __tablename__ = 'tip'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    date = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
