from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from app.workout.core.settings.redis_settings import RedisConfig


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(
            self, redis_config: RedisConfig
    ) -> AsyncIterable[Redis]:
        redis = Redis.from_url(redis_config.dsn, decode_responses=True)
        yield redis
        await redis.close()
