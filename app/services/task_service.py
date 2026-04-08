from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Task, User, Project, RoleCode, TaskSubmission, TaskStatus
from app.schemas.task import TaskSubmitRequest


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, data, manager: User):

        # 🔴 project tekshirish
        project = self.db.get(Project, data.project_id)
        if not project:
            raise HTTPException(404, "Project not found")

        # 🔴 ownership check
        if project.manager_id != manager.id:
            raise HTTPException(403, "Not your project")

        # 🔴 worker tekshirish
        worker = self.db.get(User, data.assigned_to_id)
        if not worker:
            raise HTTPException(404, "Worker not found")

        if worker.role != RoleCode.worker:
            raise HTTPException(400, "User is not a worker")

        # 🔴 deadline validation
        now = datetime.now(timezone.utc)

        if data.deadline_at < now:
            raise HTTPException(400, "Deadline must be in the future")

        task = Task(
            project_id=data.project_id,
            title=data.title,
            description=data.description,
            assigned_by_id=manager.id,
            assigned_to_id=data.assigned_to_id,
            deadline_at=data.deadline_at,
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task
    
    def get_worker_tasks(self, worker: User):
        return (
            self.db.query(Task)
            .filter(Task.assigned_to_id == worker.id)
            .all()
        )
    
    def submit_task(self, task_id: int, worker: User, data: TaskSubmitRequest):

        task = self.db.get(Task, task_id)

        if not task:
            raise HTTPException(404, "Task not found")

        # ❗ ownership
        if task.assigned_to_id != worker.id:
            raise HTTPException(403, "Not your task")

        # ❗ already submitted
        if task.submission:
            raise HTTPException(400, "Task already submitted")

        # 🔥 STATUS LOGIC (ENG MUHIM QISM)
        now = datetime.utcnow()

        if task.deadline_at < now:
            task.status = TaskStatus.late
        else:
            task.status = TaskStatus.submitted

        submission = TaskSubmission(
            task_id=task.id,
            worker_id=worker.id,
            text_content=data.text_content,
        )

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission