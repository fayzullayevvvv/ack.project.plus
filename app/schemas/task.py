from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    project_id: int
    title: str = Field(min_length=3)
    description: Optional[str] = None
    assigned_to_id: int
    deadline_at: datetime


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    deadline_at: datetime
    assigned_to_id: int
    project_id: int

    class Config:
        from_attributes = True


class TaskSubmitRequest(BaseModel):
    text_content: Optional[str] = None