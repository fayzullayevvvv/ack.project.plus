from typing import Annotated

from fastapi import APIRouter, status, Depends, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.models import user
from app.schemas.auth import UserLoginResponse, RefreshRequest, ChangePasswordRequest
from app.schemas.user import UserResponseDetail
from app.core.deps import get_db, get_user
from app.services.user_service import UserService
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
def login_view(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    db: Annotated[Session, Depends(get_db)],
):
    user_service = UserService(db)
    login_response = user_service.authenticate_user(credentials)

    return login_response


@router.post(
    "/refresh", response_model=UserLoginResponse, status_code=status.HTTP_200_OK
)
def refresh_view(
    data: Annotated[RefreshRequest, Body()], db: Annotated[Session, Depends(get_db)]
):
    user_service = UserService(db)
    refresh_response = user_service.refresh_access_token(data.refresh_token)
    return refresh_response


@router.post("/logout")
def logout(
    refresh_token: str,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    service = UserService(db)
    service.logout(refresh_token)

    return {"message": "Logged out"}


@router.post("/change-password")
def change_password_view(
    data: ChangePasswordRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user)],
):
    service = UserService(db)

    service.change_password_current_user(
        user=current_user,
        old_password=data.old_password,
        new_password=data.new_password,
    )

    return {"message": "Password changed successfully"}


@router.post("/me", response_model=UserResponseDetail)
async def get_me(current_user: Annotated[User, Depends(get_user)]):
    return current_user
