from pydantic import BaseModel, Field


class Price(BaseModel):
    price: int = Field(ge=0)
    currency: str = Field(min_length=1)
