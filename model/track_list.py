from typing import Optional

from pydantic import BaseModel

from .artist import Artist


class TrackList(BaseModel):
    url: str
    title: str
    image: Optional[str]
    artists: list[Artist]
