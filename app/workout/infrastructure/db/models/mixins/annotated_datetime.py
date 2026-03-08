import datetime as dt
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column


def date_time_column(nullable: bool = True) -> mapped_column:
    """Factory for all datetime columns that won't change on update"""
    return Annotated[
        dt.datetime,
        mapped_column(
            sa.DateTime(timezone=True),
            nullable=nullable,
            server_default=sa.func.now(),
            default=lambda: dt.datetime.now(dt.UTC),
        ),
    ]
