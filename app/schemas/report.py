from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserResponse
from app.schemas.task import TaskResponse
from app.schemas.project import ProjectResponse
from app.models import MonthlyReportStatus


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


class MonthlyReportItem(BaseModel):
    report_id: int
    report_date: date
    text: Optional[str]


class MonthlyReportResponse(BaseModel):
    user_id: int
    project_id: int
    year: int
    month: int
    total_reports: int
    reports: list[MonthlyReportItem]


class MonthlyReportSubmitResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    year: int
    month: int
    total_reports: int
    submitted_at: datetime
    status: MonthlyReportStatus

    reports: list[ReportResponse] = []

    model_config = ConfigDict(from_attributes=True)