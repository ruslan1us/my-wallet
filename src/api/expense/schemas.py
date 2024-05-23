from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    name: str
    amount: float
    description: Optional[str] = None
    expense_place: int


class ExpenseRead(BaseModel):
    id: int
    name: str
    amount: float
    expensed_at: Optional[datetime] = datetime.utcnow
    description: Optional[str] = None


class ExpenseUpdate(BaseModel):
    name: str
    amount: float
    description: Optional[str] = None
    expensed_at: Optional[datetime] = datetime.utcnow
    expense_place: int


class MoneySpinnerCreate(BaseModel):
    name: str


class MoneySpinnerReadWithoutExpenses(MoneySpinnerCreate):
    id: int


class MoneySpinnerReadWithExpenses(MoneySpinnerReadWithoutExpenses):
    expenses: List[ExpenseRead]


class SubscriptionCreate(BaseModel):
    name: str
    amount: float


class SubscriptionRead(BaseModel):
    id: int
    name: str
    amount: float
