from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    func
)

from app.db.base import Base, TimeStampMixin


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    roles: Mapped[List["Role"]] = relationship(
        secondary="user_roles",
        back_populates="users",
        lazy="selectin",
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
    task_submissions: Mapped[List["TaskSubmission"]] = relationship(back_populates="worker")