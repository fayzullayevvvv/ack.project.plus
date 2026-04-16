from typing import Annotated

from fastapi import APIRouter, Depends, Body, UploadFile, File, Path
from sqlalchemy.orm import Session

from app.schemas.report import (
    CreateDailyReport,
    ReportResponse,
    ReportDetailResponse,
    UpdateReportRequest,
)
from app.core.deps import get_db, get_worker, get_user
from app.models import User
from app.services.report_service import ReportService


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/daily", response_model=ReportResponse, status_code=201)
def create_daily_report_view(
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
def get_reports_view(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    service = ReportService(db)
    return service.get_reports(user=user)


@router.get("/daily/{id}", response_model=ReportDetailResponse)
def get_report_view(
    id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    service = ReportService(db)
    return service.get_report(id, user)


@router.patch(
    "/daily/{id}",
    response_model=ReportResponse,
)
def update_report_view(
    id: Annotated[int, Path()],
    data: Annotated[UpdateReportRequest, Body()],
    db: Annotated[Session, Depends(get_db)],
    worker: Annotated[User, Depends(get_worker)],
):
    service = ReportService(db)
    return service.update_report(report_id=id, data=data, user=worker)
