from app.workout.application.common.transactional import transactional
from app.workout.domains.protocols.iuow import IUnitOfWork


class CleanupInteractor:
    """Celery interface for cleanup the database
     from an expired refresh tokens."""

    def __init__(self, uow: IUnitOfWork) -> None:
        self.UoW = uow

    @transactional
    async def execute(self) -> None:
        await self.UoW.refresh_repository.delete_expired()
