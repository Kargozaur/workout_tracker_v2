from uuid import uuid7

from . import UUID, Mapped, mapped_column, sa

IDTypes = int | UUID


class IdMixin[T: IDTypes]: ...


class UUIDIdMixin(IdMixin[UUID]):
    id: Mapped[UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid7
    )


class IntIdMixin(IdMixin[int]):
    id: Mapped[int] = mapped_column(primary_key=True)
