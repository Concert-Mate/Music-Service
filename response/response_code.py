from enum import IntEnum


class ResponseCode(IntEnum):
    SUCCESS = (0,)
    INTERNAL_ERROR = (1,)
    ARTIST_NOT_FOUND = (2,)
    TRACK_LIST_NOT_FOUND = (3,)
