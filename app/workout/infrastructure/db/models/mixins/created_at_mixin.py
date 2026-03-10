from . import Mapped
from .annotated_timestamp import DateTime


class CreatedAtMixin:
    created_at: Mapped[DateTime]
