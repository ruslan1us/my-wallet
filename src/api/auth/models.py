from datetime import datetime
from sqlalchemy import String, Boolean
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.expense.models import Subscription
from src.base_maker import Base

from src.api.time_func import set_date


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=100), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=set_date)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    budget: Mapped[float] = mapped_column(nullable=True, default=0.0)
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )