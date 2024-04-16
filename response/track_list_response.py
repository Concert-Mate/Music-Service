from typing import Optional

from pydantic import BaseModel

from model import TrackList
from .response_status import ResponseStatus


class TrackListResponse(BaseModel):
    status: ResponseStatus = ResponseStatus()
    track_list: Optional[TrackList] = None
