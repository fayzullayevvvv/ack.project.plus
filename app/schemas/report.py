from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.schemas.user import UserResponse
from app.schemas.task import TaskResponse
from app.schemas.project import ProjectResponse


class CreateDailyReport(BaseModel):
    project_id: int
    task_id: int
    text: str = Field(default=None, max_length=5000)


class ReportResponse(BaseModel):
    id: int
    user_id: int
    task_id: int
    project_id: int
    text: str
    report_date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportDetailResponse(BaseModel):
    id: int
    user: UserResponse
    task: TaskResponse
    project: ProjectResponse
    text: str | None = None
    report_date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class UpdateReportRequest(BaseModel):
    text: Optional[str] = Field(default=None, max_length=5000)
