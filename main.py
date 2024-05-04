from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis.asyncio import Redis, from_url as redis_from_url
from uvicorn.config import logger as default_logger

from model import Concert, TrackList
from response import ResponseCode, TrackListResponse, ConcertsResponse, ResponseStatus
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
        default_logger.warning(f'Failed to initialize redis cache: {e}')


async def shutdown() -> None:
    await yandex_music_service.terminate()
    await redis.close()


app: FastAPI = FastAPI(
    on_startup=[startup],
    on_shutdown=[shutdown],
)


@app.get('/concerts')
@cache(expire=settings.concerts_expiration_time)
async def get_concerts(artist_id: int) -> ConcertsResponse:
    status: ResponseStatus

    try:
        concerts: list[Concert] = await yandex_music_service.parse_concerts(artist_id)
        return ConcertsResponse(concerts=concerts)
    except NotFoundException as e:
        status = ResponseStatus(
            code=ResponseCode.ARTIST_NOT_FOUND,
            message=str(e),
        )
    except InternalServiceErrorException as e:
        status = ResponseStatus(
            code=ResponseCode.ARTIST_NOT_FOUND,
            message=str(e),
        )

    return ConcertsResponse(status=status)


@app.get('/track-lists')
@cache(expire=settings.track_lists_expiration_time)
async def get_tracks_list_info(url: str) -> TrackListResponse:
    status: ResponseStatus

    try:
        track_list: TrackList = await yandex_music_service.parse_track_list(url)
        return TrackListResponse(track_list=track_list)
    except NotFoundException as e:
        status = ResponseStatus(
            code=ResponseCode.TRACK_LIST_NOT_FOUND,
            message=str(e),
        )
    except InternalServiceErrorException as e:
        status = ResponseStatus(
            code=ResponseCode.INTERNAL_ERROR,
            message=str(e),
        )

    return TrackListResponse(status=status)
