from sqlalchemy.orm import Session

from app.models import Task, TaskAssignment, DailyReport, User


class ReportRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs):
        report = DailyReport(**kwargs)
        self.db.add(report)
        return report

    def get_report_by_user(self, user_id: int) -> list[DailyReport]:
        return (
            self.db.query(DailyReport)
            .join(User, User.id == DailyReport.user_id)
            .filter(DailyReport.user_id == user_id)
            .all()
        )

    def exists(self, user_id, project_id, report_date):
        return (
            self.db.query(DailyReport.id)
            .filter(
                DailyReport.user_id == user_id,
                DailyReport.project_id == project_id,
                DailyReport.report_date == report_date,
            )
            .first()
            is not None
        )
    
    def get_all(self):
        return self.db.query(DailyReport).all()
    
    def get_by_projects(self, project_ids: list[int]):
        return (
            self.db.query(DailyReport)
            .filter(DailyReport.project_id.in_(project_ids))
            .order_by(DailyReport.report_date.desc())
            .all()
        )