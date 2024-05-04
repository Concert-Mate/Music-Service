from pydantic import BaseModel, Field


class Artist(BaseModel):
    name: str = Field(min_length=1)
    yandex_music_id: int = Field(ge=0)

    class Config:
        frozen = True
