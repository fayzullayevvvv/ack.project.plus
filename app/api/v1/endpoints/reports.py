from typing import Annotated

from fastapi import APIRouter, Depends, Body, UploadFile, File
from sqlalchemy.orm import Session

from app.schemas.report import CreateDailyReport, ReportResponse
from app.core.deps import get_db, get_worker, get_user
from app.models import User
from app.services.report_service import ReportService


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/daily", response_model=ReportResponse, status_code=201)
def create_daily_report(
    data: Annotated[CreateDailyReport, Body()],
    db: Annotated[Session, Depends(get_db)],
    worker: Annotated[User, Depends(get_worker)],
):
    service = ReportService(db)

    return service.create_daily_report(
        user=worker,
        data=data,
    )


@router.get(
    "/daily",
    response_model=list[ReportResponse],
)
def get_reports(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    service = ReportService(db)
    return service.get_reports(user=user)