from fastapi import FastAPI
from uvicorn import run
from app.settings import settings
from app.services import YandexMusicService
from app.routes import ConcertsRouter


async def on_startup() -> None:
    await yandex_music_service.setup()


async def on_shutdown() -> None:
    await yandex_music_service.terminate()


yandex_music_service = YandexMusicService()
app: FastAPI = FastAPI(
    on_startup=[on_startup],
    on_shutdown=[on_shutdown]
)
app.include_router(ConcertsRouter(yandex_music_service).router)


if __name__ == '__main__':
    run(app=app, host=settings.host, port=settings.port)
