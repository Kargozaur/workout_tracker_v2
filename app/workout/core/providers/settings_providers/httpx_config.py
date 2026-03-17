from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from httpx import AsyncClient, AsyncHTTPTransport, Limits


class HttpxProvider(Provider):
    @provide(scope=Scope.APP)
    def get_limits(self) -> Limits:
        return Limits(max_connections=10, max_keepalive_connections=5)

    @provide(scope=Scope.REQUEST)
    async def get_client(self, limits: Limits) -> AsyncIterator[AsyncClient]:
        transport = AsyncHTTPTransport(retries=3)
        async with AsyncClient(
            transport=transport,
            limits=limits,
            headers={"Accept": "application/json"},
            timeout=10,
            follow_redirects=True,
        ) as client:
            yield client
