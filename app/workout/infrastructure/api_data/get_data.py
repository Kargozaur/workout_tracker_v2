# import asyncio
import time
from urllib.parse import urlparse

from httpx import AsyncClient
from loguru import logger

from app.workout.domains.entities.httpx_response import ResponseSchema


class APIData:
    def __init__(
        self,
        client: AsyncClient,
        url: str = "https://exercisedb.dev/api/v1/exercises",
    ) -> None:
        self.client = client
        self.__api_url = url
        self.__base_domain = self._get_domain(self.__api_url)

    @staticmethod
    def _get_domain(url: str) -> str:
        return urlparse(url).netloc

    @property
    def api(self) -> str:
        return self.__api_url

    @api.setter
    def api(self, new_url: str) -> None:
        domain = self._get_domain(new_url)
        if domain != self.__base_domain:
            raise ValueError(
                f"Domain {self.__base_domain} expected, instead got: {domain}"
            )
        self.__api_url = new_url

    async def get_data(self, offset: int = 0, limit: int = 10) -> ResponseSchema | None:
        logger.info(f"requesting {self.api}")
        start = time.perf_counter()
        response = await self.client.get(
            self.api, params={"offset": offset, "limit": limit}
        )
        if response.status_code == 200:
            logger.info(
                f"response status code: {response.status_code}.\n"
                f"Response_time: {time.perf_counter() - start:.2f}ms"
            )
            data = ResponseSchema.model_validate_json(response.text)
            return data
        return None


# async def get_data():
#     async with AsyncClient() as aclient:
#         new_data = APIData(aclient)
#         res = await new_data.get_data()
#     return res
#
#
# print(asyncio.run(get_data()))
