from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import UserRepository
from app.core.security import hash_password
from app.schemas.admin_user import AdminUpdateUser


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db=self.db)

    def create_user(
        self,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        role: str,
        password: str,
    ) -> User:

        existing = self.repo.get_by_email(email)
        if existing:
            raise HTTPException(400, "Email already exists")

        existing = self.repo.get_by_username(username)
        if existing:
            raise HTTPException(400, "Username already exists")

        password = hash_password(password)

        return self.repo.create_user(
            first_name, last_name, username, email, role, password
        )

    def get_user_by_id(self, user_id) -> User:
        user = self.db.get(User, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def update_user(self, user_id: int, data: AdminUpdateUser):

        user = self.db.get(User, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # username check
        if data.username and data.username != user.username:
            if self.repo.get_by_username(data.username):
                raise HTTPException(400, "Username already exists")

        # email check
        if data.email and data.email != user.email:
            if self.repo.get_by_email(data.email):
                raise HTTPException(400, "Email already exists")

        # update fields
        if data.first_name:
            user.first_name = data.first_name

        if data.last_name:
            user.last_name = data.last_name

        if data.username:
            user.username = data.username

        if data.email:
            user.email = data.email

        if data.role:
            user.role = data.role

        if data.password:
            user.password_hash = hash_password(data.password)

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(self, user_id: int):

        user = self.db.get(User, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="User already deleted")

        user.is_active = False

        self.db.commit()

        return {"detail": "User deactivated"}
