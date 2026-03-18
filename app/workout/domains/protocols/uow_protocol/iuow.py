from typing import Protocol, Self, runtime_checkable

from app.workout.domains.protocols.repository_protocols.iexerciserepository import (
    IExerciseRepository,
)
from app.workout.domains.protocols.repository_protocols.irefresh_repository import (
    IRefreshRepository,
)
from app.workout.domains.protocols.repository_protocols.iuser_repository import (
    IUserRepository,
)
from app.workout.domains.protocols.repository_protocols.iworkout_items_repository import (  # noqa: E501
    IWorkoutItems,
)
from app.workout.domains.protocols.repository_protocols.iworkout_repository import (
    IWorkoutRepository,
)


@runtime_checkable
class IUnitOfWork(Protocol):
    """Interface for all IUnitOfWork implementations.
    Commits must be explicit."""

    user_repository: IUserRepository
    refresh_repository: IRefreshRepository
    workout_repository: IWorkoutRepository
    exercise_repository: IExerciseRepository
    workout_items_repository: IWorkoutItems

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
