from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.entities.refresh_token_schema import (
    RefreshTokenSchema,
)
from app.workout.domains.protocols.irefresh_repository import (
    IRefreshRepository,
)
from app.workout.infrastructure.db.models.refresh_token import RefreshToken

from . import BaseRepository


class RefreshTokenRepository(
    BaseRepository[RefreshToken, RefreshTokenSchema, None],
    IRefreshRepository[RefreshToken, RefreshTokenSchema],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RefreshToken)

    async def get_refresh_token(self, **filters) -> RefreshToken:
        return await super().get_entity(**filters)

    async def create_refresh_token(
            self, data: RefreshTokenSchema
    ) -> RefreshToken:
        return await super().create_entity(data)

    async def revoke_refresh_token(self, **filters) -> bool:
        return await super().delete_entity(**filters)
