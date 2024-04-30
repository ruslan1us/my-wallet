from pydantic import Field, BaseModel, EmailStr
from src.api.time_func import set_year
from typing import List, Dict, Any



class Month(BaseModel):
    month: int = Field(ge=1, le=12)


class Year(BaseModel):
    year: int = Field(default=set_year(), ge=2000, le=2100)


class Day(BaseModel):
    day: int = Field(ge=1, le=31)


class EmailSchema(BaseModel):
    subject: str
    email_to: List[EmailStr]
    body: Dict[str, Any]
