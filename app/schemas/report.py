from datetime import date, datetime

from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: int
    user_id: int
    task_id: int
    project_id: int
    text: str
    report_date: date
    created_at: datetime
