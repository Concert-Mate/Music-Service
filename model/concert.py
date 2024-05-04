from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .artist import Artist
from .price import Price


class Concert(BaseModel):
    title: str
    afisha_url: str
    city: str
    place: Optional[str]
    address: str
    datetime: datetime
    map_url: Optional[str]
    images: list[str]
    min_price: Optional[Price]
    artists: list[Artist] = Field(min_length=1)
