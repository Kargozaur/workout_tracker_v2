from dataclasses import dataclass


@dataclass
class CategoryToId:
    category_to_id: dict[str, int]
