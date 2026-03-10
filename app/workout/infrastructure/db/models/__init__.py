from app.workout.infrastructure.db.models.base import Base
from app.workout.infrastructure.db.models.mixins.annotated_timestamp import (
    DateTime,
)
from app.workout.infrastructure.db.models.mixins.created_at_mixin import (
    CreatedAtMixin,
)
from app.workout.infrastructure.db.models.mixins.id_mixin import (
    IntIdMixin,
    UUIDIdMixin,
)
from app.workout.infrastructure.db.models.mixins.updated_at_mixin import (
    UpdatedAtMixin,
)
