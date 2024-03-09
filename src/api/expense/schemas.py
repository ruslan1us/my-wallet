from typing import Optional

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP


class ExpenseCreate(BaseModel):
    name: str
    amount: float
    description: Optional[str] = None
    expensed_at: TIMESTAMP
    expensed_at: int


class ExpenseRead(ExpenseCreate):
    id: int


class MoneySpinnerCreate(BaseModel):
    name: str


class MoneySpinnerRead(MoneySpinnerCreate):
    id: int
