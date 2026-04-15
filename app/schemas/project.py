from datetime import date

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.project import ProjectStatus


class ProjectResponse(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    manager_id: Optional[int]
    status: Optional[str]
    deadline: Optional[datetime]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    deadline: date
    manager_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    deadline: date
    manager_id: int
    status: ProjectStatus

    class Config:
        from_attributes = True
