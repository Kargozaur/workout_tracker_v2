from dataclasses import dataclass


@dataclass
class Slice[T]:
    items: list[T]
    page: int
    size: int
    has_next: bool
