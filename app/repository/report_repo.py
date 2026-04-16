from sqlalchemy.orm import Session

from app.models import Task, TaskAssignment, DailyReport, User


class ReportRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_report_by_user(self, user_id: int) -> list[DailyReport]:
        return (
            self.db.query(DailyReport)
            .join(User, User.id == DailyReport.user_id)
            .filter(DailyReport.user_id == user_id)
            .all()
        )
