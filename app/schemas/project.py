from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectResponse(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    manager_id: Optional[int]
    status: Optional[str]
    deadline: Optional[datetime]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
