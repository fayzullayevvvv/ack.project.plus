from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_admin
from app.schemas.user import CreateUser, UserResponse
from app.services import UserService
from app.models import User


router = APIRouter(tags=["Admin"])


@router.post(
    "/v1/admin/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user_view(
    data: Annotated[CreateUser, Body()],
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    user_service = UserService(db)

    user = user_service.create_user(
        full_name=data.full_name,
        username=data.username,
        email=data.email,
        role=data.role,
        password=data.password,
    )

    return user
