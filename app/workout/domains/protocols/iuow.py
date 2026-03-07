from . import Protocol, runtime_checkable
from .irefresh_repository import IRefreshRepository
from .iuser_repository import IUserRepository


@runtime_checkable
class IUnitOfWork(Protocol):
    """Interface for all IUnitOfWork implementations.
    Commits must be explicit."""

    user_repository: IUserRepository
    refresh_repository: IRefreshRepository

    def __aenter__(self) -> None: ...

    def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
