from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.help_request import HelpRequestStatus


class HelpRequestCreate(BaseModel):
    task_id: int = Field(..., gt=0)


class HelpRequestResponse(BaseModel):
    id: int = Field(..., gt=0)
    task_id: int = Field(..., gt=0)
    requested_by: int = Field(..., gt=0)
    status: HelpRequestStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str
