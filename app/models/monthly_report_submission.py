from datetime import datetime
import enum

from sqlalchemy import Integer, ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models import Base


class MonthlyReportStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class MonthlyReportSubmission(Base):
    __tablename__ = "monthly_report_submissions"

    __table_args__ = (
        UniqueConstraint(
            "user_id", "project_id", "year", "month",
            name="uq_user_project_month"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False, index=True
    )
    year: Mapped[int]
    month: Mapped[int]
    total_reports: Mapped[int] = mapped_column(default=0)
    status: Mapped[MonthlyReportStatus] = mapped_column(
        Enum(MonthlyReportStatus),
        default=MonthlyReportStatus.DRAFT,
        nullable=False
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User")
    project: Mapped["Project"] = relationship("Project")
    