from sqlalchemy.orm import Session

from app.models import Project, User
from app.schemas.project import CreateProject


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, data: CreateProject, manager: User) -> Project:
        project = Project(
            name=data.name,
            description=data.description,
            start_date=data.start_date,
            end_date=data.end_date,
            manager_id=manager.id,
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project
    
    def get_manager_projects(self, manager: User) -> Project:
         return (
            self.db.query(Project)
            .filter(Project.manager_id == manager.id)
            .all()
        )
    
    def get_project_by_id(self, id: int) -> Project:
        return self.db.query(Project).filter(Project.id == id).first()