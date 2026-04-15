from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.task import TaskStatus


class TaskResponse(BaseModel):
    id: Optional[int]
    project_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]
    deadline: Optional[datetime]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
