from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import User, UserRole
from app.schemas.task import CreateTask, UpdateTask
from app.repository.task_repo import TaskRepo
from app.repository.project_repo import ProjectRepo


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepo(db)
        self.project_repo = ProjectRepo(db)

    def create_task(self, data: CreateTask, project_id: int):
        project = self.project_repo.get_project_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )

        task = self.task_repo.create(
            project_id=project_id,
            title=data.title,
            description=data.description,
            deadline=data.deadline,
        )
        return task
    
    def update_task(self, task_id: int, data: UpdateTask, manager):
        task = self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if task.project.manager_id != manager.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed",
            )

        update_data = data.model_dump(exclude_unset=True)

        if "status" in update_data:
            new_status = update_data["status"]

            if not task.status.can_transition(new_status):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status transition: {task.status} → {new_status}",
                )

        return self.task_repo.update(task, update_data)

    def get_tasks(self, user: User):
        if user.role == "admin":
            return self.task_repo.get_all_tasks()

        if user.role == "manager":
            return self.task_repo.get_by_manager(user.id)

        if user.role == "worker":
            return self.task_repo.get_tasks_by_user(user.id)

        return []

    def get_task(self, task_id: int, user: User):
        task = self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if user.role == "admin":
            return task

        if user.role == "manager":
            if task.project.manager_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not allowed",
                )
            return task

        if user.role == "worker":
            is_assigned = self.task_repo.get_assignment(task.id, user.id)

            if not is_assigned:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not allowed",
                )

            return task
