from typing import Optional

from pydantic import BaseModel, Field

from .artist import Artist


class TrackList(BaseModel):
    url: str = Field(min_length=1)
    title: str = Field(min_length=1)
    image: Optional[str] = None
    artists: list[Artist]
