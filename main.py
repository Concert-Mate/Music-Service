from fastapi import FastAPI

from model import Concert, TracksList
from services import YandexMusicService


async def on_startup() -> None:
    await yandex_music_service.setup()


async def on_shutdown() -> None:
    await yandex_music_service.terminate()


yandex_music_service = YandexMusicService()
app: FastAPI = FastAPI(
    on_startup=[on_startup],
    on_shutdown=[on_shutdown]
)


@app.get('/concerts', response_model=list[Concert])
async def get_concerts(artist_id: int) -> list[Concert]:
    return await yandex_music_service.parse_concerts(artist_id)


@app.get('/tracks-lists', response_model=TracksList)
async def get_tracks_list_info(url: str) -> TracksList:
    return await yandex_music_service.parse_tracks_list(url)
