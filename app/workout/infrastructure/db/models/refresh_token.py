import datetime as dt
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, CreatedAtMixin, UUIDIdMixin


class RefreshToken(UUIDIdMixin, CreatedAtMixin, Base):
    __tablename__ = "refresh_tokens"

    token_hash: Mapped[str] = mapped_column(sa.String(100))
    expires_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.UTC),
        server_default=sa.func.now(),
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("user.id", ondelete="CASCADE")
    )

    owned_by = relationship("User", back_populates="refresh_tokens")
