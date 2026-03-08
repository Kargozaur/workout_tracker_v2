from typing import Protocol, runtime_checkable

from app.workout.domains.protocols.repository_protocols.irefresh_repository import (
    IRefreshRepository,
)
from app.workout.domains.protocols.repository_protocols.iuser_repository import (
    IUserRepository,
)
from app.workout.domains.protocols.repository_protocols.iworkout_repository import IWorkoutRepository

@runtime_checkable
class IUnitOfWork(Protocol):
    """Interface for all IUnitOfWork implementations.
    Commits must be explicit."""

    user_repository: IUserRepository
    refresh_repository: IRefreshRepository
    workout_repository: IWorkoutRepository
    def __aenter__(self) -> None: ...

    def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
