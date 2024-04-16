from pydantic import BaseModel, Field

from .response_code import ResponseCode


class ResponseStatus(BaseModel):
    code: ResponseCode = Field(
        default=ResponseCode.SUCCESS,
        description=''.join([f'{i} - {ResponseCode(i).name}, ' for i in range(len(ResponseCode))])
    )

    message: str = ResponseCode.SUCCESS.name
