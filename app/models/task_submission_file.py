import enum
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Enum, DateTime, func

from app.db.base import Base


class FileType(str, enum.Enum):
    image = "image"
    file = "file"
    pdf = "pdf"
    docx = "docx"
    xlsx = "xlsx"
    txt = "txt"


class TaskSubmissionFile(Base):
    __tablename__ = "task_submission_files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("task_submissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[FileType] = mapped_column(
        Enum(FileType, name="file_type"), nullable=False
    )
    original_name: Mapped[Optional[str]] = mapped_column(String(255))
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    submission: Mapped["TaskSubmission"] = relationship(back_populates="files")
