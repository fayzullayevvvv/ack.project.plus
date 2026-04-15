from typing import Annotated

from fastapi import APIRouter, status, Depends, Body, Path
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import (
    UserResponseDetail,
    CreateUser,
    UserResponse,
    UpdateUserData,
)
from app.schemas.auth import ChangePasswordRequest
from app.core.deps import get_admin, get_manager, get_db, get_admin_or_manager, get_user
from app.services.user_service import UserService
from app.repository.user_repo import UserRepo

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", response_model=UserResponse, status_code=201)
def create_user_view(
    data: Annotated[CreateUser, Body()],
    manager: Annotated[User, Depends(get_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    user = service.create_user(data)
    return user


@router.get("/", response_model=list[UserResponse])
def get_users_view(
    admin: Annotated[User, Depends(get_admin)], db: Annotated[Session, Depends(get_db)]
):
    repository = UserRepo(db)
    users = repository.get_all_users()

    return users


@router.get("/{id}", response_model=UserResponseDetail)
def get_user_view(
    id: Annotated[int, Path()],
    admin_or_manager: Annotated[User, Depends(get_admin_or_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    user = service.get_user_by_id(id)

    return user


@router.patch("/{id}", response_model=UserResponse)
def update_user_view(
    id: Annotated[int, Path()],
    data: Annotated[UpdateUserData, Body()],
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    updated_user = service.update_user(id, data, user)

    return updated_user


@router.patch("/{id}/activate", response_model=UserResponse)
async def activate_user_view(
    id: Annotated[int, Path()],
    admin_or_manager: Annotated[User, Depends(get_admin_or_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    activated_user = service.activate_user(id)

    return activated_user


@router.patch("/{id}/deactivate", response_model=UserResponse)
def deactivate_user_view(
    id: Annotated[int, Path()],
    admin_or_manager: Annotated[User, Depends(get_admin_or_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    deactivated_user = service.deactivate_user(id)

    return deactivated_user


@router.post("/{id}/reset-password")
def reset_password_view(
    id: Annotated[int, Path()],
    data: Annotated[ChangePasswordRequest, Body()],
    admin_or_manager: Annotated[User, Depends(get_admin_or_manager)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    service.reset_password(id, data)

    return {"message": "succesfully changed"}
