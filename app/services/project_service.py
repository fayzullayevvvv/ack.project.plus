from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Project, User


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, data, manager: User):

        # optional validation
        if data.end_date and data.start_date:
            if data.end_date < data.start_date:
                raise HTTPException(400, "End date cannot be before start date")

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
    
    def get_manager_projects(self, manager: User):
        return (
            self.db.query(Project)
            .filter(Project.manager_id == manager.id)
            .all()
        )