from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func, DateTime


class Base(DeclarativeBase):
    pass


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
