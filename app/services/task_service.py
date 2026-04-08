from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Task, User, Project, RoleCode, TaskSubmission, TaskStatus
from app.schemas.task import TaskSubmitRequest, CreateTask
from app.repositories.project_repo import ProjectRepository
from app.repositories.task_repo import TaskRepository
from app.repositories.user_repo import UserRepository


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.project_repo = ProjectRepository(db=self.db)
        self.task_repo = TaskRepository(db=self.db)
        self.user_repo = UserRepository(db=self.db)

    def create_task(self, data: CreateTask, manager: User) -> Task:

        project = self.project_repo.get_project_by_id(id=data.project_id)
        if not project:
            raise HTTPException(404, "Project not found")

        if project.manager_id != manager.id:
            raise HTTPException(403, "Not your project")

        worker = self.user_repo.get_user_by_id(id=data.assigned_to_id)
        if not worker:
            raise HTTPException(404, "Worker not found")

        if worker.role != RoleCode.worker:
            raise HTTPException(400, "User is not a worker")

        now = datetime.now(timezone.utc)

        if data.deadline_at <= now + timedelta(seconds=1):
            raise HTTPException(400, "Deadline must be in the future")

        return self.task_repo.create_task(data=data, manager=manager)
    
    def submit_task(self, task_id: int, worker: User, data: TaskSubmitRequest):

        task = self.task_repo.get_task_by_id(task_id)

        if not task:
            raise HTTPException(404, "Task not found")

        if task.assigned_to_id != worker.id:
            raise HTTPException(403, "Not your task")

        if task.status in [TaskStatus.submitted, TaskStatus.late]:
            raise HTTPException(400, "Task already submitted")

        now = datetime.now(timezone.utc)

        if now > task.deadline_at:
            task.status = TaskStatus.late
        else:
            task.status = TaskStatus.submitted

        return self.task_repo.task_submission(data=data, worker=worker, task=task)