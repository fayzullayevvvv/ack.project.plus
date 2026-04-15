from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repository.project_repo import ProjectRepo
from app.models.project import Project
from app.models.user import User, UserRole
from app.models.project import ProjectStatus


class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepo(db)

    def create_project(
        self,
        name: str,
        description: str | None,
        deadline,
        manager_id: int,
        created_by: int,
        current_user_role: str,
    ):
        if current_user_role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin can create project",
            )

        manager = self.repo.get_user_by_id(manager_id)
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manager not found",
            )

        if manager.role != UserRole.MANAGER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user must have manager role",
            )

        project = Project(
            name=name,
            description=description,
            deadline=deadline,
            manager_id=manager_id,
            status=ProjectStatus.ASSIGNED,
        )

        return self.repo.create_project(project)

    def get_projects(self, user: User):

        if user.role == UserRole.ADMIN:
            return self.repo.get_all_projects()

        elif user.role == UserRole.MANAGER:
            return self.repo.get_projects_by_manager(user.id)

        elif user.role == UserRole.WORKER:
            return self.repo.get_projects_by_user(user.id)

        return []

    def get_project_detail(self, project_id: int, user):

        project = self.repo.get_project_by_id(project_id)

        if not project:
            raise HTTPException(404, "Project not found")

        if user.role == UserRole.ADMIN:
            return project

        if user.role == UserRole.MANAGER:
            if project.manager_id != user.id:
                raise HTTPException(403, "Access denied")
            return project

        if user.role == UserRole.WORKER:
            is_member = self.repo.is_project_member(project_id, user.id)

            if not is_member:
                raise HTTPException(403, "Access denied")

            return project

        raise HTTPException(403, "Access denied")
