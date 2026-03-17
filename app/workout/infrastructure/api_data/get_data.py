import asyncio
import time
from collections.abc import AsyncGenerator
from urllib.parse import urlparse

from httpx import AsyncClient
from loguru import logger

from app.workout.domains.entities.httpx_response import ResponseSchema


class APIData:
    def __init__(
        self,
        client: AsyncClient,
    ) -> None:
        self.client = client
        self.__api_url = "https://exercisedb.dev/api/v1/exercises"
        self.__base_domain = self._get_domain(self.__api_url)

    @staticmethod
    def _get_domain(url: str) -> str:
        return urlparse(url).netloc

    async def get_data(
        self, url: str, params: dict[str, int] | None = None
    ) -> ResponseSchema | None:
        if self._get_domain(url) != self.__base_domain:
            raise
        try:
            logger.info(f"requesting {url}")
            start = time.perf_counter()
            response = await self.client.get(url, params=params, timeout=10)
            if response.status_code == 200:
                logger.info(
                    f"response status code: {response.status_code}.\n"
                    f"Response_time: {time.perf_counter() - start:.2f}ms"
                )
                data: ResponseSchema = ResponseSchema.model_validate_json(response.text)
                return data
        except Exception as exc:
            logger.error(f"Request failed for {url}: {exc}")
        return None

    async def fetch_all(self, limit: int = 10) -> AsyncGenerator[ResponseSchema]:
        current_url: str = self.__api_url
        params: dict[str, int] | None = {"offset": 0, "limit": limit}
        while current_url:
            await asyncio.sleep(3)
            data: ResponseSchema | None = await self.get_data(current_url, params)
            if not data:
                break

            yield data
            current_url: str = data.metadata.next_page
            params = None
