from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_admin, get_db, get_user
from app.schemas.project import ProjectCreateRequest, ProjectResponse
from app.services.project_service import ProjectService
from app.models.user import User


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin)],
):
    service = ProjectService(db)

    project = service.create_project(
        name=data.name,
        description=data.description,
        deadline=data.deadline,
        manager_id=data.manager_id,
        created_by=current_user.id,
        current_user_role=current_user.role,
    )

    return project


@router.get("", response_model=List[ProjectResponse], status_code=status.HTTP_200_OK)
def get_projects(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Session, Depends(get_user)],
):
    service = ProjectService(db)

    projects = service.get_projects(current_user)

    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Session, Depends(get_user)],
):
    service = ProjectService(db)

    project = service.get_project_detail(project_id, current_user)

    return project
