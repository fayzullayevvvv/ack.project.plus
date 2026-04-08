from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Project, User
from app.repositories.project_repo import ProjectRepository
from app.schemas.project import CreateProject


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjectRepository(db=self.db)