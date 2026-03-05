from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.entities.refresh_token_schema import (
    RefreshTokenSchema,
)
from app.workout.domains.exceptions.entity_exceptions import (
    EntityDeletionException,
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

    async def create_refresh_token(
            self, data: RefreshTokenSchema
    ) -> RefreshToken:
        return await super().create_entity(data)

    async def revoke_refresh_token(self, user_id: UUID) -> bool:
        query = sa.select(RefreshToken).where(RefreshToken.user_id == user_id)
        try:
            await self.session.execute(query)
            return True
        except Exception as exc:
            raise EntityDeletionException() from exc
