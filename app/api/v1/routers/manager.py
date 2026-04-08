from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_manager
from app.schemas.project import CreateProject, ProjectResponse
from app.services.project_service import ProjectService
from app.repositories.project_repo import ProjectRepository
from app.models import User, Project

router = APIRouter(prefix="/v1/manager", tags=["Manager Projects"])


@router.post("/projects", response_model=ProjectResponse)
def create_project_view(
    data: CreateProject,
    manager: Annotated[User, Depends(get_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    repository = ProjectRepository(db)
    return repository.create_project(data, manager)


@router.get("/projects", response_model=List[ProjectResponse])
def get_projects_view(
    manager: Annotated[User, Depends(get_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    repository = ProjectRepository(db)
    return repository.get_manager_projects(manager)


