from uuid import UUID

from pydantic import BaseModel
from redis.asyncio import Redis

from app.workout.domains.protocols.icacheservice import ICacheService


class CacheService[R: BaseModel, T: str | None](ICacheService[R, T]):
    def __init__(self, redis: Redis, model: type[R]) -> None:
        self.redis = redis
        self.model = model

    async def get_cache(
            self,
            user_id: UUID,
    ) -> R | None:
        cache: T = await self.redis.get(f"user:{user_id}")
        if not cache:
            return None
        return self.model.model_validate_json(cache)

    async def set_cache(self, user_id: UUID, cache_attributes: R) -> None:
        await self.redis.set(
            f"user:{user_id}", cache_attributes.model_dump_json(), ex=600
        )

    async def delete_cache(self, user_id: UUID) -> None:
        await self.redis.delete(f"user:{user_id}")
