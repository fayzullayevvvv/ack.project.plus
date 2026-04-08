from datetime import datetime

from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date


class CreateProject(BaseModel):
    name: str = Field(min_length=3)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("End date cannot be before start date")
        return self


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