from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.protocols.iuow import IUnitOfWork
from app.workout.infrastructure.uow import UnitOfWork


class UnitOfWorkProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_uow(self, session: AsyncSession) -> IUnitOfWork:
        return UnitOfWork(session)
