from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP


class ExpenseCreate(BaseModel):
    name: str
    amount: float
    description: Optional[str] = None
    # expensed_at: Optional[datetime] = datetime.utcnow
    expense_place: int


class ExpenseRead(ExpenseCreate):
    id: int
    expensed_at: Optional[datetime] = datetime.utcnow


class MoneySpinnerCreate(BaseModel):
    name: str


class MoneySpinnerRead(MoneySpinnerCreate):
    id: int
