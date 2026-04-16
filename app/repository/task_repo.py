from sqlalchemy.orm import Session

from app.models import Task, TaskAssignment, Project
from app.schemas.task import CreateTask


class TaskRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs):
        task = Task(**kwargs)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task
    
    def update(self, task: Task, data: dict):
        for key, value in data.items():
            setattr(task, key, value)

        self.db.commit()
        self.db.refresh(task)
        return task

    def get_tasks_by_user(self, user_id: int) -> list[Task]:
        return (
            self.db.query(Task)
            .join(Task.assignments)
            .filter(TaskAssignment.user_id == user_id)
            .all()
        )

    def get_all_tasks(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_by_manager(self, manager_id: int) -> list[Task]:
        return (
            self.db.query(Task)
            .join(Project, Project.id == Task.project_id)
            .filter(Project.manager_id == manager_id)
            .all()
        )

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_assignment(self, task_id: int, user_id: int):
        return (
            self.db.query(TaskAssignment)
            .filter(
                TaskAssignment.task_id == task_id,
                TaskAssignment.user_id == user_id,
            )
            .first()
        )
