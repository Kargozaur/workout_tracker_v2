from dataclasses import dataclass


@dataclass
class MuscleGroupToId:
    group_to_id: dict[str, int]
