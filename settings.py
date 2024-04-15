from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str = ''
    concerts_expiration_time: int = 60
    track_lists_expiration_time: int = 600

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
