from datetime import date, datetime, timedelta
from fastapi import HTTPException, status

from app.repository.report_repo import ReportRepo
from app.repository.task_repo import TaskRepo
from app.repository.project_repo import ProjectRepo
from app.models import User, UserRole
from app.schemas.report import CreateDailyReport


class ReportService:
    def __init__(self, db):
        self.db = db
        self.repo = ReportRepo(db)
        self.task_repo = TaskRepo(db)
        self.project_repo = ProjectRepo(db)

    def create_daily_report(self, user: User, data: CreateDailyReport):
        task = self.task_repo.get_by_id(data.task_id)

        if not task or task.project_id != data.project_id:
            raise HTTPException(400, "Invalid task for this project")

        if not self.project_repo.is_project_member(data.project_id, user.id):
            raise HTTPException(
                403,
                "You are not assigned to this project",
            )

        if not self.task_repo.get_assignment(data.task_id, user.id):
            raise HTTPException(
                403,
                "You are not assigned to this task",
            )

        if self.repo.exists(user.id, data.project_id, data.report_date):
            raise HTTPException(400, "Report already exists for this day")

        return self.repo.create(
            user_id=user.id,
            project_id=data.project_id,
            task_id=data.task_id,
            text=data.text,
        )

    def update_report(self, report_id: int, data, user):
        report = self.repo.get_by_id(report_id)

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found",
            )

        if report.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only report owner can update",
            )

        now = datetime.utcnow()
        if report.created_at < now - timedelta(hours=24):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Report can only be edited within 24 hours",
            )

        update_data = {}

        if data.text is not None:
            update_data["text"] = data.text

        return self.repo.update(report, update_data)

    def get_reports(self, user):
        if user.role == UserRole.ADMIN:
            return self.repo.get_all()

        if user.role == UserRole.MANAGER:
            project_ids = self.project_repo.get_user_project_ids(user.id)

            if not project_ids:
                return []

            return self.repo.get_by_projects(project_ids)

        if user.role == UserRole.WORKER:
            return self.repo.get_report_by_user(user.id)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    def get_report(self, report_id: int, user):
        report = self.repo.get_by_id(report_id)

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found",
            )

        if user.role == UserRole.ADMIN:
            return report

        if user.role == UserRole.MANAGER:
            if not self.project_repo.is_project_member(report.project_id, user.id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )
            return report

        if user.role == UserRole.WORKER:
            if report.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )
            return report

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
