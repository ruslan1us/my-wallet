from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP


class SalaryCreate(BaseModel):
    name: str
    amount: float


class SalaryRead(SalaryCreate):
    id: int
    date: Optional[datetime] = datetime.utcnow


class TipCreate(BaseModel):
    amount: float


class TipRead(TipCreate):
    id: int
    date: Optional[datetime] = datetime.utcnow

