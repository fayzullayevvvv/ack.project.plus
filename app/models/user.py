from typing import List, Optional
from datetime import datetime
import enum

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, DateTime, Enum, func

from app.db.base import Base, TimeStampMixin


class RoleCode(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    worker = "worker"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleCode] = mapped_column(
        Enum(RoleCode, name="role_enum"),
        nullable=False,
        index=True,
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False,
)

    profile: Mapped[Optional["Profile"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    skills: Mapped[List["Skill"]] = relationship(
        secondary="user_skills",
        back_populates="users",
        lazy="selectin",
    )

    projects_managed: Mapped[List["Project"]] = relationship(
        back_populates="manager",
        foreign_keys="Project.manager_id",
    )

    assigned_tasks: Mapped[List["Task"]] = relationship(
        back_populates="assignee",
        foreign_keys="Task.assigned_to_id",
    )

    created_tasks: Mapped[List["Task"]] = relationship(
        back_populates="assigner",
        foreign_keys="Task.assigned_by_id",
    )

    daily_reports: Mapped[List["DailyReport"]] = relationship(back_populates="user")
    task_submissions: Mapped[List["TaskSubmission"]] = relationship(
        back_populates="worker"
    )
