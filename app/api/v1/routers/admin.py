from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.user import CreateUser, UserResponse
from app.services import UserService


router = APIRouter(tags=["Admin"])


@router.post("/v1/admin/users", response_model=UserResponse, status_code=201)
async def create_user_view(
    data: Annotated[CreateUser, Body()], db: Annotated[Session, Depends(get_db)]
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
