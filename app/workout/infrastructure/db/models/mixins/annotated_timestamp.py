import datetime as dt
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column


DateTime = Annotated[
    dt.datetime,
    mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.UTC),
        server_default=sa.func.now(),
    ),
]
"""Annotated datetime for the sqlalchemy DateTime columns."""
