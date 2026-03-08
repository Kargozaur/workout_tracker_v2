from enum import StrEnum


class WorkoutStatuses(StrEnum):
    SCHEDULED = "scheduled"
    SKIPPED = "skipped"
    FINISHED = "finished"
