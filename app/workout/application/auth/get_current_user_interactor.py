from typing import Any
from uuid import UUID

from app.workout.application.common.read_only import read_only
from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.exceptions.user_exceptions import (
    UserNotFoundException,
)
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.iuow import IUnitOfWork


class GetUserInteractor[T]:
    def __init__(
        self,
        uow: IUnitOfWork,
        access_token: AccessToken,
        token_provider: ITokenProvider,
    ) -> None:
        self.UoW = uow
        self.access_token = access_token
        self.token_provider = token_provider

    @read_only
    async def execute(self) -> T:
        decoded_token: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: str = decoded_token.get("sub")
        user_data: T | None = await self.UoW.user_repository.get_user(
            id=UUID(user_id),
            fields=(
                "id",
                "email",
                "first_name",
                "last_name",
                "created_at",
                "updated_at",
            ),
        )
        if not user_data:
            raise UserNotFoundException("User not found")
        return user_data
