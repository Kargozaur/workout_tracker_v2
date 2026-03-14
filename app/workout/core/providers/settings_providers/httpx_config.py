from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from httpx import AsyncClient


class HttpxProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_client(self) -> AsyncIterator[AsyncClient]:
        async with AsyncClient(
            headers={"Accept": "application/json"}, timeout=10
        ) as client:
            yield client
