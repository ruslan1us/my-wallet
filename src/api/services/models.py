from pydantic import Field, BaseModel
from src.api.time_func import set_year


class Month(BaseModel):
    month: int = Field(ge=1, le=12)


class Year(BaseModel):
    year: int = Field(default=set_year(), ge=2000, le=2100)


class Day(BaseModel):
    day: int = Field(ge=1, le=31)
