from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self,
        first_name: str,
        last_name,
        username: str,
        email: str,
        role: str,
        hash_password: str,
    ) -> User:
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            role=role,
            password_hash=hash_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_all_users(self, is_active=None, skip=0, limit=10, search=None):
        query = self.db.query(User)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        if search:
            query = query.filter(
                (User.username.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
            )

        return query.offset(skip).limit(limit).all()
