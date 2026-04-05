from typing import Optional
from datetime import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    DateTime,
    Enum,
    func
)

from app.db.base import Base, TimeStampMixin


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    submitted = "submitted"
    done = "done"
    cancelled = "cancelled"


class Task(Base, TimeStampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id: Mapped[Optional[int]] = mapped_column(ForeignKey("task_templates.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    assigned_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    assigned_to_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)

    deadline_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),
        default=TaskStatus.pending,
        nullable=False,
        index=True,
    )

    project: Mapped["Project"] = relationship(back_populates="tasks")
    template: Mapped[Optional["TaskTemplate"]] = relationship(back_populates="tasks")
    assigner: Mapped["User"] = relationship(back_populates="created_tasks", foreign_keys=[assigned_by_id])
    assignee: Mapped["User"] = relationship(back_populates="assigned_tasks", foreign_keys=[assigned_to_id])

    submission: Mapped[Optional["TaskSubmission"]] = relationship(
        back_populates="task",
        uselist=False,
        cascade="all, delete-orphan",
    )