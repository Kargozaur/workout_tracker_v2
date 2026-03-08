from . import Mapped
from .annotated_datetime import date_time_column


class CreatedAtMixin:
    created_at: Mapped[date_time_column(False)]
