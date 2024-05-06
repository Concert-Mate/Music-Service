import logging.config
from http import HTTPStatus
from typing import Optional

import starlette.datastructures
import starlette.middleware.base
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis.asyncio import Redis, from_url as redis_from_url
from starlette.requests import Request

from model import Concert, TrackList
from response import ResponseCode, TrackListResponse, ConcertsResponse, ResponseStatus
from services import NotFoundException, InternalServiceErrorException
from services import YandexMusicService
from settings import settings

logging.config.fileConfig(fname='logging.ini')
root_logger = logging.getLogger('root')
service_logger: logging.Logger = logging.getLogger('service')
controller_logger: logging.Logger = logging.getLogger('controller')

yandex_music_service = YandexMusicService(service_logger)
redis: Redis = redis_from_url(
    f'redis://:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}'
)


def log_return_success(url: starlette.datastructures.URL) -> None:
    controller_logger.info(f'Returning SUCCESS for {url}')


def log_return_error(url: starlette.datastructures.URL, status: ResponseStatus) -> None:
    controller_logger.info(f'Returning {status.code} - "{status.message}" for {url}')


async def startup() -> None:
    root_logger.info('Application is launching ...')
    await yandex_music_service.setup()

    # If connection fail, server will continue working, but without caching
    root_logger.info('Initializing redis-backend ...')
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    root_logger.info('Redis-backend is initialized')

    try:
        root_logger.info('Checking connection with redis ...')
        await redis.ping()  # Check redis connection and auth
        root_logger.info('Connection with Redis is OK')
    except Exception as e:
        root_logger.warning('Failed to establish connection with redis : %s', e)


async def shutdown() -> None:
    root_logger.critical('Application is shutting down ...')
    await yandex_music_service.terminate()
    await redis.close()


app: FastAPI = FastAPI(
    on_startup=[startup],
    on_shutdown=[shutdown],
)


@app.middleware('http')
async def log_middleware(request: Request, call_next):
    client: Optional[starlette.datastructures.Address] = request.client

    controller_logger.info(
        f'Received %s %s from %s:%s',
        request.method,
        request.url,
        None if client is None else client.host,
        None if client is None else client.port,
    )

    result = await call_next(request)

    if result.status_code == HTTPStatus.NOT_MODIFIED:
        controller_logger.info(f'Returning response from cache for {request.url}')

    return result


@app.get('/concerts')
@cache(expire=settings.concerts_expiration_time)
async def get_concerts(request: Request, artist_id: int) -> ConcertsResponse:
    request_url: starlette.datastructures.URL = request.url
    status: ResponseStatus

    try:
        concerts: list[Concert] = await yandex_music_service.parse_concerts(artist_id)
        log_return_success(request_url)
        return ConcertsResponse(concerts=concerts)
    except NotFoundException:
        status = ResponseStatus(
            code=ResponseCode.ARTIST_NOT_FOUND,
            message=f'Artist {artist_id} not found',
        )
    except InternalServiceErrorException:
        status = ResponseStatus(
            code=ResponseCode.ARTIST_NOT_FOUND,
            message='Internal service error',
        )

    log_return_error(url=request_url, status=status)
    return ConcertsResponse(status=status)


@app.get('/track-lists')
@cache(expire=settings.track_lists_expiration_time)
async def get_tracks_list_info(request: Request, url: str) -> TrackListResponse:
    request_url: starlette.datastructures.URL = request.url
    status: ResponseStatus

    try:
        track_list: TrackList = await yandex_music_service.parse_track_list(url)
        log_return_success(request_url)
        return TrackListResponse(track_list=track_list)
    except NotFoundException:
        status = ResponseStatus(
            code=ResponseCode.TRACK_LIST_NOT_FOUND,
            message=f'Track list {url} not found',
        )
    except InternalServiceErrorException:
        status = ResponseStatus(
            code=ResponseCode.INTERNAL_ERROR,
            message='Internal service error',
        )

    log_return_error(url=request_url, status=status)
    return TrackListResponse(status=status)
