from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository.analytics_repo import AnalyticsRepo
from app.models.user import User, UserRole
from app.models.task import Task
from app.models.project import Project
from app.models.help_request import HelpRequestStatus


class AnalyticsService:
    def __init__(self, db: Session):
        self.repo = AnalyticsRepo(db)

    def get_admin_dashboard(self, current_user: User):
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(403, "Only admin can access admin dashboard")

        total_users, active_users = self.repo.count_users()
        total_projects, active_projects = self.repo.count_projects()
        total_tasks, completed_tasks = self.repo.count_tasks()
        pending_help_requests = self.repo.count_pending_help_requests()
        unread_notifications = self.repo.count_unread_notifications(current_user.id)

        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_projects": total_projects,
            "active_projects": active_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_help_requests": pending_help_requests,
            "unread_notifications": unread_notifications,
        }

    def get_manager_dashboard(self, current_user: User):
        if current_user.role != UserRole.MANAGER:
            raise HTTPException(403, "Only manager can access manager dashboard")

        total_projects = len(self.repo.get_manager_projects(current_user.id))
        active_projects = (
            sum(1 for p in self.repo.get_manager_projects(current_user.id) if p.status == "active")
        )
        total_workers = self.repo.count_manager_workers(current_user.id)
        total_tasks = self.repo.count_manager_tasks(current_user.id)
        completed_tasks = self.repo.count_manager_completed_tasks(current_user.id)
        pending_help_requests = self.repo.count_pending_help_requests()
        unread_notifications = self.repo.count_unread_notifications(current_user.id)

        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "total_workers": total_workers,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_help_requests": pending_help_requests,
            "unread_notifications": unread_notifications,
        }

    def get_worker_dashboard(self, current_user: User):
        if current_user.role != UserRole.WORKER:
            raise HTTPException(403, "Only worker can access worker dashboard")

        total_assigned_tasks = self.repo.count_tasks_for_user(current_user.id)
        active_tasks = self.repo.count_active_tasks_for_user(current_user.id)
        completed_tasks = self.repo.count_completed_tasks_for_user(current_user.id)
        blocked_tasks = self.repo.count_blocked_tasks_for_user(current_user.id)
        overdue_tasks = self.repo.count_overdue_tasks_for_user(current_user.id)
        pending_help_requests = 0
        unread_notifications = self.repo.count_unread_notifications(current_user.id)

        return {
            "total_assigned_tasks": total_assigned_tasks,
            "active_tasks": active_tasks,
            "completed_tasks": completed_tasks,
            "blocked_tasks": blocked_tasks,
            "overdue_tasks": overdue_tasks,
            "pending_help_requests": pending_help_requests,
            "unread_notifications": unread_notifications,
        }

    def get_workload(self, current_user: User):
        if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
            raise HTTPException(403, "Access denied")

        rows = self.repo.get_workload_rows()
        result = []
        for row in rows:
            result.append(
                {
                    "user_id": row.user_id,
                    "username": row.username,
                    "assigned_tasks": int(row.assigned_tasks or 0),
                    "active_tasks": int(row.active_tasks or 0),
                    "completed_tasks": int(row.completed_tasks or 0),
                    "blocked_tasks": int(row.blocked_tasks or 0),
                    "overdue_tasks": int(row.overdue_tasks or 0),
                }
            )
        return result

    def get_deadlines(self, current_user: User):
        if current_user.role == UserRole.ADMIN:
            rows = self.repo.get_deadline_rows()
        elif current_user.role == UserRole.MANAGER:
            rows = self.repo.get_deadline_rows()
        elif current_user.role == UserRole.WORKER:
            rows = self.repo.get_deadline_rows(user_id=current_user.id)
        else:
            raise HTTPException(403, "Access denied")

        now = datetime.utcnow()
        result = []
        for row in rows:
            result.append(
                {
                    "entity_type": "task",
                    "entity_id": row.entity_id,
                    "title": row.title,
                    "deadline": row.deadline,
                    "status": row.status.value if hasattr(row.status, "value") else str(row.status),
                    "is_overdue": row.deadline < now if row.deadline else False,
                }
            )
        return result

    def get_reports(self, current_user: User):
        if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
            raise HTTPException(403, "Access denied")

        return {
            "total_daily_reports": self.repo.count_reports_total(),
            "reports_today": self.repo.count_reports_today(),
            "reports_this_month": self.repo.count_reports_this_month(),
            "unique_reporters": self.repo.count_unique_reporters(),
        }

    def get_project_progress(self, current_user: User):
        if current_user.role == UserRole.ADMIN:
            rows = self.repo.get_project_progress_rows()
        elif current_user.role == UserRole.MANAGER:
            rows = self.repo.get_project_progress_rows(manager_id=current_user.id)
        else:
            raise HTTPException(403, "Access denied")

        result = []
        for row in rows:
            total = int(row.total_tasks or 0)
            completed = int(row.completed_tasks or 0)
            progress = 0.0
            if total > 0:
                progress = (completed / total) * 100

            result.append(
                {
                    "project_id": row.project_id,
                    "project_name": row.project_name,
                    "total_tasks": total,
                    "completed_tasks": completed,
                    "progress": round(progress, 2),
                }
            )
        return result