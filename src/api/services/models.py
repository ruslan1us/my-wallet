from pydantic import Field, BaseModel


class Month(BaseModel):
    month: int = Field(ge=1, le=12)


class Year(BaseModel):
    year: int = Field(ge=2000, le=2100)


class Day(BaseModel):
    day: int = Field(ge=1, le=31)
