from typing import Any
from uuid import UUID

from loguru import logger

from app.workout.application.common.types.token_types import AccessToken
from app.workout.application.workouts.queries.get_single_workout import (
    GetSingleWorkout,
)
from app.workout.domains.entities.workout_schema import WorkoutCache
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.service_protocols.icacheservice import (
    ICacheService,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class GetCachedWorkout[T](GetSingleWorkout):
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
        interactor: GetSingleWorkout,
        service: ICacheService[WorkoutCache],
    ) -> None:
        super().__init__(uow, token_provider, access_token)
        self.interactor = interactor
        self.service = service

    async def execute(self, workout_id: UUID) -> WorkoutCache:
        user_data: dict[str, Any] = self.token_provider.decode_token(self.access_token)
        user_id: str = user_data.get("sub")  # type: ignore
        cached: WorkoutCache | None = await self.service.get_cache(
            f"{user_id}:{workout_id}"
        )
        if cached:
            logger.info("Cache hit for a single workout.")
            return cached
        not_cached: T | None = await self.interactor.execute(workout_id)
        cache_data: WorkoutCache = WorkoutCache(**not_cached.__dict__)
        await self.service.set_cache(f"{user_id}:{workout_id}", cache_data)
        logger.debug("Set cache for a single workout.")
        return not_cached
