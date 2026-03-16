from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork
from app.workout.infrastructure.repositories.exercise_repository import (
    ExerciseRepository,
)
from app.workout.infrastructure.repositories.refresh_repository import (
    RefreshTokenRepository,
)
from app.workout.infrastructure.repositories.user_repository import (
    UserRepository,
)
from app.workout.infrastructure.repositories.workout_repository import (
    WorkoutRepository,
)


class UnitOfWork(IUnitOfWork):
    """Unit of Work implementation of the IUnitOfWork interface.
    Sessions are managed by the dishka.
    Commits must be explicit."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository: UserRepository = UserRepository(session)
        self.refresh_repository: RefreshTokenRepository = RefreshTokenRepository(
            session
        )
        self.workout_repository: WorkoutRepository = WorkoutRepository(session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        if exc_val:
            await self.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
