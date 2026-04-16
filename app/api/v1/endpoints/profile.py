from typing import Annotated

from fastapi import APIRouter, Depends, Body, UploadFile, File
from sqlalchemy.orm import Session

from app.schemas.user_profile import UserProfile, UpdateProfile
from app.models import User
from app.repository.user_repo import UserRepo
from app.services.user_service import UserService

from app.core.deps import get_user, get_db

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=UserProfile | None)
def user_profile_view(
    db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_user)]
):
    return user.profile


@router.post("/me", response_model=UserProfile)
def update_profile_view(
    data: Annotated[UpdateProfile, Body()],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    repository = UserRepo(db)
    updated_profile = repository.update_profile(data=data, user=user)

    return updated_profile


@router.post("/avatar", response_model=UserProfile)
def avatar_profile(
    file: Annotated[UploadFile, File(...)],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    service = UserService(db)
    return service.update_avatar(user=user, file=file)
