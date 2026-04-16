from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import Integer, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models import Base


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    task_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tasks.id"), nullable=True, index=True
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False, index=True
    )
    text: Mapped[Optional[str]] = mapped_column(Text)
    report_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    attachments: Mapped[List["ReportAttachment"]] = relationship(
        "ReportAttachment", back_populates="report", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship("User")
    task: Mapped[Optional["Task"]] = relationship("Task")
    project: Mapped["Project"] = relationship("Project")
