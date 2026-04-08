from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateProject(BaseModel):
    name: str = Field(min_length=3)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    start_date: Optional[date]
    end_date: Optional[date]
    created_at: datetime

    class Config:
        from_attributes = True