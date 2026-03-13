from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryToId:
    _category_to_id: dict[str, int]

    def get(self, name: str) -> int | None:
        return self._category_to_id.get(name, None)
