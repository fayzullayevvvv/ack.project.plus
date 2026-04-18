from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_user
from app.models.user import User
from app.schemas.dashboard import (
    DashboardAdminResponse,
    DashboardManagerResponse,
    DashboardWorkerResponse,
    WorkloadItemResponse,
    DeadlineItemResponse,
    ReportAnalyticsResponse,
    ProjectProgressItemResponse,
)
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["Analytics"])


dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@dashboard_router.get("/admin", response_model=DashboardAdminResponse)
def admin_dashboard(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    return AnalyticsService(db).get_admin_dashboard(current_user)


@dashboard_router.get("/manager", response_model=DashboardManagerResponse)
def manager_dashboard(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    return AnalyticsService(db).get_manager_dashboard(current_user)


@dashboard_router.get("/worker", response_model=DashboardWorkerResponse)
def worker_dashboard(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    return AnalyticsService(db).get_worker_dashboard(current_user)


@router.get("/workload", response_model=List[WorkloadItemResponse])
def workload(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    return AnalyticsService(db).get_workload(current_user)


@router.get("/deadlines", response_model=List[DeadlineItemResponse])
def deadlines(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    return AnalyticsService(db).get_deadlines(current_user)


@router.get("/reports", response_model=ReportAnalyticsResponse)
def reports(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    return AnalyticsService(db).get_reports(current_user)


@router.get("/project-progress", response_model=List[ProjectProgressItemResponse])
def project_progress(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    return AnalyticsService(db).get_project_progress(current_user)