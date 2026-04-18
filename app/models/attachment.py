from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class ReportAttachment(Base):
    __tablename__ = "report_attachments"

    __table_args__ = (
    UniqueConstraint("report_id", "file_id", name="uq_report_file"),
)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("daily_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    report: Mapped["DailyReport"] = relationship(
        "DailyReport",
        back_populates="attachments"
    )
    file: Mapped["File"] = relationship(
        "File",
        lazy="joined"
    )