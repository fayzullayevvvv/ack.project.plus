from datetime import datetime, date, timedelta

from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus
from app.models.task_assignment import TaskAssignment
from app.models.daily_report import DailyReport
from app.models.help_request import HelpRequest, HelpRequestStatus
from app.models.notification import Notification


class AnalyticsRepo:
    def __init__(self, db: Session):
        self.db = db

    def count_users(self):
        total = self.db.query(func.count(User.id)).scalar() or 0
        active = (
            self.db.query(func.count(User.id))
            .filter(User.is_active == True)
            .scalar()
            or 0
        )
        return total, active

    def count_projects(self):
        total = self.db.query(func.count(Project.id)).scalar() or 0
        active = (
            self.db.query(func.count(Project.id))
            .filter(Project.status == ProjectStatus.ACTIVE)
            .scalar()
            or 0
        )
        return total, active

    def count_tasks(self):
        total = self.db.query(func.count(Task.id)).scalar() or 0
        completed = (
            self.db.query(func.count(Task.id))
            .filter(Task.status == TaskStatus.DONE)
            .scalar()
            or 0
        )
        return total, completed

    def count_pending_help_requests(self):
        return (
            self.db.query(func.count(HelpRequest.id))
            .filter(HelpRequest.status == HelpRequestStatus.PENDING)
            .scalar()
            or 0
        )

    def count_unread_notifications(self, user_id: int):
        return (
            self.db.query(func.count(Notification.id))
            .filter(Notification.user_id == user_id, Notification.is_read == False)
            .scalar()
            or 0
        )

    def count_workers(self):
        return (
            self.db.query(func.count(User.id))
            .filter(User.role == UserRole.WORKER)
            .scalar()
            or 0
        )

    def count_active_tasks_for_user(self, user_id: int):
        return (
            self.db.query(func.count(TaskAssignment.id))
            .join(Task, Task.id == TaskAssignment.task_id)
            .filter(
                TaskAssignment.user_id == user_id,
                Task.status.in_(list(TaskStatus.active_statuses())),
            )
            .scalar()
            or 0
        )

    def count_tasks_for_user(self, user_id: int):
        return (
            self.db.query(func.count(TaskAssignment.id))
            .join(Task, Task.id == TaskAssignment.task_id)
            .filter(TaskAssignment.user_id == user_id)
            .scalar()
            or 0
        )

    def count_completed_tasks_for_user(self, user_id: int):
        return (
            self.db.query(func.count(TaskAssignment.id))
            .join(Task, Task.id == TaskAssignment.task_id)
            .filter(TaskAssignment.user_id == user_id, Task.status == TaskStatus.DONE)
            .scalar()
            or 0
        )

    def count_blocked_tasks_for_user(self, user_id: int):
        return (
            self.db.query(func.count(TaskAssignment.id))
            .join(Task, Task.id == TaskAssignment.task_id)
            .filter(TaskAssignment.user_id == user_id, Task.status == TaskStatus.BLOCKED)
            .scalar()
            or 0
        )

    def count_overdue_tasks_for_user(self, user_id: int):
        now = datetime.utcnow()
        return (
            self.db.query(func.count(TaskAssignment.id))
            .join(Task, Task.id == TaskAssignment.task_id)
            .filter(
                TaskAssignment.user_id == user_id,
                Task.deadline.isnot(None),
                Task.deadline < now,
                Task.status.notin_([TaskStatus.DONE, TaskStatus.CANCELED]),
            )
            .scalar()
            or 0
        )

    def get_manager_projects(self, manager_id: int):
        return self.db.query(Project).filter(Project.manager_id == manager_id).all()

    def count_manager_tasks(self, manager_id: int):
        return (
            self.db.query(func.count(Task.id))
            .join(Project, Project.id == Task.project_id)
            .filter(Project.manager_id == manager_id)
            .scalar()
            or 0
        )

    def count_manager_completed_tasks(self, manager_id: int):
        return (
            self.db.query(func.count(Task.id))
            .join(Project, Project.id == Task.project_id)
            .filter(Project.manager_id == manager_id, Task.status == TaskStatus.DONE)
            .scalar()
            or 0
        )

    def count_manager_workers(self, manager_id: int):
        return (
            self.db.query(func.count(func.distinct(TaskAssignment.user_id)))
            .join(Task, Task.id == TaskAssignment.task_id)
            .join(Project, Project.id == Task.project_id)
            .filter(Project.manager_id == manager_id)
            .scalar()
            or 0
        )

    def get_workload_rows(self):
        return (
            self.db.query(
                User.id.label("user_id"),
                User.username.label("username"),
                func.count(TaskAssignment.id).label("assigned_tasks"),
                func.sum(
                    func.case(
                        (Task.status.in_(list(TaskStatus.active_statuses())), 1),
                        else_=0,
                    )
                ).label("active_tasks"),
                func.sum(
                    func.case((Task.status == TaskStatus.DONE, 1), else_=0)
                ).label("completed_tasks"),
                func.sum(
                    func.case((Task.status == TaskStatus.BLOCKED, 1), else_=0)
                ).label("blocked_tasks"),
                func.sum(
                    func.case(
                        (
                            Task.deadline.isnot(None),
                            func.case(
                                (
                                    Task.deadline < datetime.utcnow(),
                                    func.case(
                                        (
                                            Task.status.notin_(
                                                [TaskStatus.DONE, TaskStatus.CANCELED]
                                            ),
                                            1,
                                        ),
                                        else_=0,
                                    ),
                                ),
                                else_=0,
                            ),
                        ),
                        else_=0,
                    )
                ).label("overdue_tasks"),
            )
            .join(TaskAssignment, TaskAssignment.user_id == User.id)
            .join(Task, Task.id == TaskAssignment.task_id)
            .group_by(User.id, User.username)
            .all()
        )

    def get_deadline_rows(self, user_id: int | None = None):
        q = (
            self.db.query(
                Task.id.label("entity_id"),
                Task.title.label("title"),
                Task.deadline.label("deadline"),
                Task.status.label("status"),
            )
            .filter(Task.deadline.isnot(None))
            .filter(Task.status.notin_([TaskStatus.DONE, TaskStatus.CANCELED]))
        )

        if user_id is not None:
            q = q.join(TaskAssignment, TaskAssignment.task_id == Task.id).filter(
                TaskAssignment.user_id == user_id
            )

        return q.order_by(Task.deadline.asc()).all()

    def count_reports_total(self):
        return self.db.query(func.count(DailyReport.id)).scalar() or 0

    def count_reports_today(self):
        today = date.today()
        return (
            self.db.query(func.count(DailyReport.id))
            .filter(DailyReport.report_date == today)
            .scalar()
            or 0
        )

    def count_reports_this_month(self):
        today = date.today()
        return (
            self.db.query(func.count(DailyReport.id))
            .filter(
                extract("year", DailyReport.report_date) == today.year,
                extract("month", DailyReport.report_date) == today.month,
            )
            .scalar()
            or 0
        )

    def count_unique_reporters(self):
        return (
            self.db.query(func.count(func.distinct(DailyReport.user_id)))
            .scalar()
            or 0
        )

    def get_project_progress_rows(self, manager_id: int | None = None):
        q = (
            self.db.query(
                Project.id.label("project_id"),
                Project.name.label("project_name"),
                func.count(Task.id).label("total_tasks"),
                func.sum(
                    func.case((Task.status == TaskStatus.DONE, 1), else_=0)
                ).label("completed_tasks"),
            )
            .join(Task, Task.project_id == Project.id)
            .group_by(Project.id, Project.name)
        )

        if manager_id is not None:
            q = q.filter(Project.manager_id == manager_id)

        return q.all()