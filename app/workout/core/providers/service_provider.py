from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from app.workout.domains.entities.user_schemas import GetUser
from app.workout.domains.protocols.icacheservice import ICacheService
from app.workout.domains.services.cache_service import CacheService


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_cache_service(self, redis: Redis) -> ICacheService:
        return CacheService(redis, GetUser)
