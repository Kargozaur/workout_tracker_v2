from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.entities.refresh_token_schema import (
    RefreshTokenSchema,
)
from app.workout.domains.protocols.auth_protocols.irefresh_repository import (
    IRefreshRepository,
)
from app.workout.infrastructure.db.models.refresh_token import RefreshToken

from . import BaseRepository


class RefreshTokenRepository(
    BaseRepository[RefreshToken, RefreshTokenSchema, None],
    IRefreshRepository[RefreshToken, RefreshTokenSchema],
):
    """Repository for refresh tokens.
    methods get_refresh_token, create_refresh_token, delete_refresh_token
    and bulk_delete_refresh_token are used with the interactors.
    delete_expired is used in the celery worker to cleanup database
    of expired refresh tokens."""

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

    async def bulk_delete_refresh_token(self, **filters) -> None:
        await super().bulk_deletion(**filters)

    async def delete_expired(self) -> bool:
        return await super().delete_expired()
