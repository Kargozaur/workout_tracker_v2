import datetime as dt

from . import Mapped, mapped_column, sa


class CreatedAtMixin:
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow(),
        server_default=sa.func.now(),
    )
