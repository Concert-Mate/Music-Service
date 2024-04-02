from typing import Optional

from pydantic import BaseModel

from .artist import Artist


class TracksList(BaseModel):
    url: str
    title: str
    image_link: Optional[str]
    artists: list[Artist]
