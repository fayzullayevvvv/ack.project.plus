from datetime import datetime
from typing import Optional, List
import enum

from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models import Base


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELED = "canceled"

    def can_transition(self, to: "TaskStatus") -> bool:
        return to in self._transitions().get(self, set())

    @classmethod
    def _transitions(cls) -> dict["TaskStatus", set["TaskStatus"]]:
        return {
            cls.TODO: {cls.IN_PROGRESS, cls.CANCELED},
            cls.IN_PROGRESS: {cls.REVIEW, cls.BLOCKED, cls.CANCELED},
            cls.REVIEW: {cls.DONE, cls.IN_PROGRESS},
            cls.BLOCKED: {cls.IN_PROGRESS, cls.CANCELED},
        }

    @classmethod
    def active_statuses(cls) -> set["TaskStatus"]:
        return {
            cls.TODO,
            cls.IN_PROGRESS,
            cls.REVIEW,
            cls.BLOCKED,
        }

    @classmethod
    def final_statuses(cls) -> set["TaskStatus"]:
        return {
            cls.DONE,
            cls.CANCELED,
        }

    def is_final(self) -> bool:
        return self in self.final_statuses()


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.TODO
    )
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    assignments: Mapped[List["TaskAssignment"]] = relationship(
        "TaskAssignment", back_populates="task"
    )
    status_history: Mapped[List["TaskStatusHistory"]] = relationship(
        "TaskStatusHistory", back_populates="task", cascade="all, delete-orphan"
    )
