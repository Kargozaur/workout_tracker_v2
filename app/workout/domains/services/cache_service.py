from uuid import UUID

from pydantic import BaseModel
from redis.asyncio import Redis

from app.workout.application.common.types.redis_key import RedisKey
from app.workout.domains.protocols.icacheservice import ICacheService


class CacheService[R: BaseModel](ICacheService[R]):
    def __init__(
        self, redis: Redis, model: type[R], redis_key: RedisKey
    ) -> None:
        self.redis = redis
        self.model = model
        self.redis_key = redis_key

    def _get_key(self, identifier: object) -> str:
        return f"{self.redis_key}:{identifier}"

    async def get_cache(
        self,
        identifier: object,
    ) -> R | None:
        cache: str | None = await self.redis.get(self._get_key(identifier))
        if not cache:
            return None
        return self.model.model_validate_json(cache)

    async def set_cache(self, identifier: object, cache_attributes: R) -> None:
        await self.redis.set(
            self._get_key(identifier),
            cache_attributes.model_dump_json(),
            ex=600,
        )

    async def delete_cache(self, identifier: object) -> None:
        await self.redis.delete(self._get_key(identifier))
