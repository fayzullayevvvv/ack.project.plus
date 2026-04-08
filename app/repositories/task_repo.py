from sqlalchemy.orm import Session

from app.models import Project, User, Task, TaskSubmission
from app.schemas.task import CreateTask, TaskSubmitRequesta


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, data: CreateTask, manager: User) -> Task:
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
    
    def task_submission(self, data: TaskSubmitRequesta, worker: User, task: Task):
        submission = TaskSubmission(
            task_id=task.id,
            worker_id=worker.id,
            text_content=data.text_content,
        )

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission
    
    def get_task_by_id(self, id: int) -> Task:
        return self.db.query(Task).filter(Task.id == id).first()