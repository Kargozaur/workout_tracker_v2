import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, CreatedAtMixin, UpdatedAtMixin, UUIDIdMixin


class User(UUIDIdMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        sa.String(254), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    refresh_tokens = relationship(
        "RefreshToken", back_populates="owned_by", cascade="all, delete-orphan"
    )
