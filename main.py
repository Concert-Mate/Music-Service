import asyncio

from fastapi import FastAPI, HTTPException, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis, Redis

from model import Concert, TracksList
from services import NotFoundException, InternalServiceErrorException
from services import YandexMusicService
from settings import settings

yandex_music_service = YandexMusicService()
app: FastAPI = FastAPI()
redis: Redis = aioredis.from_url(f'redis://:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}')


@app.on_event("startup")
async def startup() -> None:
    await yandex_music_service.setup()

    await redis.ping()  # Check redis connection and auth
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown() -> None:
    await yandex_music_service.terminate()
    redis.close()


@app.get('/concerts')
@cache(expire=60)
async def get_concerts(artist_id: int) -> list[Concert]:
    try:
        return await yandex_music_service.parse_concerts(artist_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InternalServiceErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get('/tracks-lists')
@cache(expire=600)
async def get_tracks_list_info(url: str) -> TracksList:
    try:
        await asyncio.sleep(10)
        return await yandex_music_service.parse_tracks_list(url)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InternalServiceErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
