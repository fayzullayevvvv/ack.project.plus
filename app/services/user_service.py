import uuid

from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.repository.user_repo import UserRepo
from app.schemas.auth import UserLoginResponse
from app.schemas.user import CreateUser
from app.core.security import (
    generate_token,
    generate_refresh_token,
    verify_refresh_token,
    verify_password,
    hash_password,
)
from app.models import User


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepo(db)

    def create_user(self, data: CreateUser) -> User:
        user = self.repo.get_user_by_username(data.username)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="username already exist"
            )
        user = self.repo.get_user_by_email(data.email)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="email already exist"
            )

        data.password = hash_password(data.password)

        return self.repo.create_user(data)

    def authenticate_user(self, credentials: HTTPBasicCredentials):
        user = self.repo.get_user_by_username(credentials.username)

        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        access_token = generate_token({"sub": str(user.id)})

        refresh_jti = str(uuid.uuid4())
        refresh_token_str = generate_refresh_token(
            {"sub": str(user.id), "jti": refresh_jti}
        )

        self.repo.create_refresh_token(
            user=user, refresh_token=refresh_token_str, jti=refresh_jti
        )

        return UserLoginResponse(
            access_token=access_token, refresh_token=refresh_token_str
        )

    def refresh_access_token(self, refresh_token: str) -> UserLoginResponse:
        payload = verify_refresh_token(refresh_token)

        print(payload)

        user_id = int(payload["sub"])
        jti = payload["jti"]

        user = self.repo.get_user_by_id(user_id)
        db_token = self.repo.get_refresh_token_by_jti(jti)

        if not user or not db_token or db_token.is_revoked:
            raise HTTPException(401, "Invalid token")

        new_access = generate_token({"sub": str(user.id)})

        return UserLoginResponse(access_token=new_access, refresh_token=refresh_token)

    def logout(self, refresh_token: str):
        payload = verify_refresh_token(refresh_token)

        jti = payload.get("jti")

        db_token = self.repo.get_refresh_token_by_jti(jti)

        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        self.repo.revoke_refresh_token(db_token)

    def change_password(self, user: User, old_password: str, new_password: str):
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Old password incorrect")

        if verify_password(new_password, user.password_hash):
            raise HTTPException(
                status_code=400, detail="New password must be different"
            )

        new_hash = hash_password(new_password)

        self.repo.update_password(user, new_hash)
