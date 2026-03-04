import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, CreatedAtMixin, UUIDIdMixin


class RefreshToken(UUIDIdMixin, CreatedAtMixin, Base):
    __tablename__ = "refresh_tokens"

    token_hash: Mapped[str] = mapped_column(sa.String(100))
    expires_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )

    owned_by = relationship("User", back_populates="refresh_tokens")
