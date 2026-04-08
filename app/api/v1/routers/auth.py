from typing import Annotated

from fastapi import APIRouter, Body, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.repositories import UserRepository
from app.core.security import verify_password, generate_token

router = APIRouter(tags=["Auth"])


@router.post("/v1/login", response_model=LoginResponse)
def login_view(
    data: Annotated[LoginRequest, Body()], db: Annotated[Session, Depends(get_db)]
):
    user_repository = UserRepository(db)

    user = user_repository.get_by_username(data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token_data = {"username": user.username}
    access_token = generate_token(token_data)

    return LoginResponse(access_token=access_token)
