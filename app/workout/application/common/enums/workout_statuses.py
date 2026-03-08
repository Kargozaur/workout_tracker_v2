from enum import StrEnum


class WorkoutStatuses(StrEnum):
    SCHEDULED = "scheduled"
    SKIPPED = "skipped"
    IN_PROGRESS = "in-progress"
    FINISHED = "finished"
    CANCELLED = "cancelled"
