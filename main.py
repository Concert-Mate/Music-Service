from fastapi import FastAPI, HTTPException

from model import Concert, TracksList
from services import YandexMusicService
from services.exceptions import NotFoundException


async def on_startup() -> None:
    await yandex_music_service.setup()


async def on_shutdown() -> None:
    await yandex_music_service.terminate()


yandex_music_service = YandexMusicService()
app: FastAPI = FastAPI(
    on_startup=[on_startup],
    on_shutdown=[on_shutdown]
)


@app.get('/concerts')
async def get_concerts(artist_id: int) -> list[Concert]:
    try:
        return await yandex_music_service.parse_concerts(artist_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get('/tracks-lists')
async def get_tracks_list_info(url: str) -> TracksList:
    try:
        return await yandex_music_service.parse_tracks_list(url)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
