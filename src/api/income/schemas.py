from pydantic import BaseModel
from sqlalchemy import TIMESTAMP


class SalaryCreate(BaseModel):
    name: str
    amount: float
    date: TIMESTAMP


class SalaryRead(SalaryCreate):
    id: int
    owner_id: int


class TipCreate(BaseModel):
    amount: float
    date: TIMESTAMP


class TipRead(TipCreate):
    id: int
    owner_id: int

