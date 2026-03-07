import datetime as dt
from uuid import UUID

from . import BaseModel, Field


class RefreshTokenSchema(BaseModel):
    user_id: UUID
    token_hash: str
    expires_at: dt.datetime | None = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC) + dt.timedelta(days=7)
    )
