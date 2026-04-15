from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.task import TaskResponse


class TaskAssignmentResponse(BaseModel):
    id: Optional[int]
    task_id: Optional[int]
    user_id: Optional[int]
    assigned_by: Optional[int]
    role_on_task: Optional[str]
    assigned_at: Optional[datetime]

    task: Optional[TaskResponse]

    model_config = ConfigDict(from_attributes=True)
