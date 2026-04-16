from typing import Annotated, List

from fastapi import APIRouter, Depends, status, Path, Body
from sqlalchemy.orm import Session

from app.core.deps import get_admin, get_db, get_user, get_manager
from app.models import User
from app.schemas.task import CreateTask, TaskResponse, TaskDetailResponse, UpdateTask
from app.services.task_service import TaskService


router = APIRouter(tags=["Tasks"])


@router.post(
    "/projects/{project_id}/tasks", response_model=TaskResponse, status_code=201
)
def create_task_view(
    project_id: Annotated[int, Path()],
    data: Annotated[CreateTask, Body()],
    db: Annotated[Session, Depends(get_db)],
    manager: Annotated[User, Depends(get_manager)],
):
    service = TaskService(db)
    task = service.create_task(data, project_id)

    return task


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks_view(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    service = TaskService(db)
    tasks = service.get_tasks(user)

    return tasks


@router.get("/tasks/{id}", response_model=TaskDetailResponse)
def get_task_view(
    id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    service = TaskService(db)
    task = service.get_task(id, user)

    return task


@router.patch("/tasks/{id}", response_model=TaskResponse)
def update_task_view(
    id: Annotated[int, Path()],
    data: Annotated[UpdateTask, Body()],
    db: Annotated[Session, Depends(get_db)],
    manager: Annotated[User, Depends(get_manager)]
):
    service = TaskService(db)
    updated_task = service.update_task(id, data, manager)
    
    return updated_task