from pydantic import Field, BaseModel


class Month(BaseModel):
    month: int = Field(ge=1, le=12)