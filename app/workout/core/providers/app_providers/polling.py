from dishka import Provider, Scope, provide
from httpx import AsyncClient

from app.workout.infrastructure.api_data.get_data import APIData


class PollingProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_polling(self, client: AsyncClient) -> APIData:
        return APIData(client)
