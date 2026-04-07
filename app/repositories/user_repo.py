from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self, full_name: str, username: str, email: str, role: str, hash_password: str
    ) -> User:
        user = User(
            full_name=full_name,
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
