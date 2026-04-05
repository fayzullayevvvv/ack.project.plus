from datetime import date, datetime
from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Date,
    DateTime,
    func
)

from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    manager_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    manager: Mapped["User"] = relationship(back_populates="projects_managed")
    tasks: Mapped[List["Task"]] = relationship(back_populates="project", cascade="all, delete-orphan")