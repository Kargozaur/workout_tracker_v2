import datetime as dt

from . import Mapped, mapped_column, sa


class UpdatedAtMixin:
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), default=sa.func.now(), onupdate=sa.func.now()
    )
