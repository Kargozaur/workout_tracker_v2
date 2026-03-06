from app.workout.application.common.transactional import transactional
from app.workout.application.common.types.token_types import RefreshToken
from app.workout.domains.protocols.itokenhasher import ITokenHasher
from app.workout.domains.protocols.iuow import IUnitOfWork


class LogoutInteractor:
    def __init__(
            self,
            uow: IUnitOfWork,
            token_hasher: ITokenHasher,
            refresh_token: RefreshToken,
    ):
        self.UoW = uow
        self.token_hasher = token_hasher
        self.refresh_token = refresh_token

    @transactional
    async def execute(self) -> None:
        token_hash: str = self.token_hasher.hash(self.refresh_token)
        await self.UoW.refresh_repository.revoke_refresh_token(
            token_hash=token_hash
        )
