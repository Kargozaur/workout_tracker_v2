from typing import Any
from uuid import UUID

from loguru import logger

from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.entities.workout_schema import AddNote, WorkoutCache
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.service_protocols.icacheservice import (
    ICacheService,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class AddNoteInteractor[T]:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        service: ICacheService[WorkoutCache],
        access_token: AccessToken,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.service = service
        self.access_token = access_token

    async def execute(self, workout_id: UUID, note: AddNote) -> T:
        user_data: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: str = user_data.get("sub")
        await self.service.delete_cache(f"{user_id}:{workout_id}")
        async with self.UoW:
            logger.debug("Entered note context}")
            result = await self.UoW.workout_repository.add_note(
                note, UUID(user_id), workout_id
            )
            await self.UoW.commit()
        logger.debug("Note added")
        new_cache: WorkoutCache = WorkoutCache(**result.__dict__)
        await self.service.set_cache(f"{user_id}:{workout_id}", new_cache)
        return result
