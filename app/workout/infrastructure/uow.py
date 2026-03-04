from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.protocols.iuow import IUnitOfWork
from app.workout.infrastructure.repositories.user_repository import (
    UserRepository,
)


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository: UserRepository = UserRepository(session)

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
        await self._close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def _close(self) -> None:
        await self.session.close()
