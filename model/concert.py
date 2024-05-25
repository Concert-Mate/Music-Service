from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .artist import Artist
from .price import Price


class Concert(BaseModel):
    title: str = Field(min_length=1)
    afisha_url: str = Field(min_length=1)
    city: str = Field(min_length=1)
    place: Optional[str] = None
    address: Optional[str] = None
    concert_datetime: Optional[datetime] = None
    map_url: Optional[str] = None
    images: list[str]
    min_price: Optional[Price] = None
    artists: list[Artist] = Field(min_length=1)
