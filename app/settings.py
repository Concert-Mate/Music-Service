from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = Field(alias='PORT', default=8000)
    host: str = Field(alias='HOST', default='localhost')


settings = Settings()
