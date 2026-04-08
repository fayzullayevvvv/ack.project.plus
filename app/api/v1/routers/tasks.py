from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_manager, get_worker
from app.schemas.task import CreateTask, TaskResponse, TaskSubmitRequest
from app.services.task_service import TaskService
from app.repositories.task_repo import TaskRepository
from app.models import User, Task

router = APIRouter(prefix="/v1", tags=["Tasks"])


@router.post("/manager/tasks", response_model=TaskResponse)
def create_task_view(
    data: CreateTask,
    manager: Annotated[User, Depends(get_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    service = TaskService(db)
    return service.create_task(data, manager)


@router.get("/worker/tasks/my", response_model=List[TaskResponse])
def get_my_tasks(
    worker: Annotated[User, Depends(get_worker)],
    db: Annotated[Session, Depends(get_db)],
):
    repository = TaskRepository(db)
    return repository.get_worker_tasks(worker)


@router.post("/worker/tasks/{task_id}/submit")
def submit_task_view(
    task_id: int,
    data: TaskSubmitRequest,
    worker: Annotated[User, Depends(get_worker)],
    db: Annotated[Session, Depends(get_db)],
):
    service = TaskService(db)
    return service.submit_task(task_id, worker, data)