from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.help_request import HelpRequestStatus


class HelpRequestCreate(BaseModel):
    task_id: int


class HelpRequestResponse(BaseModel):
    id: int
    task_id: int
    requested_by: int
    status: HelpRequestStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str