from typing import Optional

from pydantic import BaseModel

from model import Concert
from .response_status import ResponseStatus


class ConcertsResponse(BaseModel):
    status: ResponseStatus = ResponseStatus()
    concerts: Optional[list[Concert]] = None
