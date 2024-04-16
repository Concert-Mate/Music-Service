from fastapi import FastAPI, HTTPException, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis.asyncio import Redis, from_url as redis_from_url
from uvicorn.config import logger

from model import Concert, TrackList
from services import NotFoundException, InternalServiceErrorException
from services import YandexMusicService
from settings import settings

yandex_music_service = YandexMusicService()
redis: Redis = redis_from_url(
    f'redis://:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}'
)


async def startup() -> None:
    await yandex_music_service.setup()

    # If connection fail, server will continue working, but without caching
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    try:
        await redis.ping()  # Check redis connection and auth
    except Exception as e:
        logger.warning(f'Failed to initialize redis cache: {e}')


async def shutdown() -> None:
    await yandex_music_service.terminate()
    await redis.close()


app: FastAPI = FastAPI(
    on_startup=[startup],
    on_shutdown=[shutdown],
)


@app.get('/concerts')
@cache(expire=settings.concerts_expiration_time)
async def get_concerts(artist_id: int) -> list[Concert]:
    try:
        return await yandex_music_service.parse_concerts(artist_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InternalServiceErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@app.get('/track-lists')
@cache(expire=settings.track_lists_expiration_time)
async def get_tracks_list_info(url: str) -> TrackList:
    try:
        return await yandex_music_service.parse_track_list(url)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InternalServiceErrorException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
