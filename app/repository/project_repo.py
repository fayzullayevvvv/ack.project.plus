from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.models.project_members import ProjectMember


class ProjectRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, id: int):
        return self.db.query(User).filter(User.id == id).first()

    def create_project(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_all_projects(self):
        return self.db.query(Project).all()

    def get_projects_by_manager(self, manager_id: int):
        return self.db.query(Project).filter(Project.manager_id == manager_id).all()

    def get_projects_by_user(self, user_id: int):
        return (
            self.db.query(Project)
            .join(ProjectMember)
            .filter(ProjectMember.user_id == user_id)
            .all()
        )

    def get_project_by_id(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def is_project_member(self, project_id: int, user_id: int) -> bool:
        return (
            self.db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id, ProjectMember.user_id == user_id
            )
            .first()
            is not None
        )
