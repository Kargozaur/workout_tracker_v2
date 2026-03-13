from dataclasses import dataclass


@dataclass(frozen=True)
class MuscleGroupToId:
    _group_to_id: dict[str, int]

    def get(self, name: str) -> int | None:
        return self._group_to_id.get(name, None)
