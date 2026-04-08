from typing import Annotated, Optional, List

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_admin
from app.schemas.user import CreateUser, UserResponse
from app.services import UserService
from app.models import User
from app.schemas.admin_user import AdminUpdateUser
from app.repositories.user_repo import UserRepository


router = APIRouter(
    prefix="/v1/admin",
    tags=["Admin"],
)


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_view(
    data: Annotated[CreateUser, Body()],
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    user_service = UserService(db)

    user = user_service.create_user(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        email=data.email,
        role=data.role,
        password=data.password,
    )

    return user


@router.get("/users", response_model=List[UserResponse])
def get_users_view(
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
    is_active: Optional[bool] = True,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    repository = UserRepository(db)
    return repository.get_all_users(
        is_active=is_active,
        skip=skip,
        limit=limit,
        search=search,
    )


@router.put(
    "/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def update_user_view(
    user_id: int,
    data: AdminUpdateUser,
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    return service.update_user(user_id, data)


@router.delete("/users/{user_id}")
def delete_user_view(
    user_id: int,
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)
    return service.delete_user(user_id)
