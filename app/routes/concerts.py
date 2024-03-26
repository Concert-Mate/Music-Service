from fastapi import APIRouter
from app.services import YandexMusicService


class ConcertsRouter:
    __yandex_music_service: YandexMusicService
    __router: APIRouter

    def __init__(self, yandex_music_service: YandexMusicService):
        self.__yandex_music_service = yandex_music_service
        self.__router = APIRouter()
        self.__add_routes()

    @property
    def router(self) -> APIRouter:
        return self.__router

    def __add_routes(self) -> None:
        self.__router.add_api_route(
            path='/concerts/',
            endpoint=self.__yandex_music_service.parse_concerts
        )
