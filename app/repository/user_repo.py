from sqlalchemy.orm import Session

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.user import CreateUser, UpdateUserData


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, data: CreateUser) -> User:
        user = User(
            username=data.username,
            email=data.email,
            role=data.role,
            password_hash=data.password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def update_user(self, id: int, data: UpdateUserData) -> User:
        user = self.get_user_by_id(id)

        if data.username:
            user.username = data.username
        if data.email:
            user.email = data.email
        if data.role:
            user.role = data.role
        if data.password:
            user.password_hash = data.password

        self.db.commit()

        return user

    def activate_user(self, user: User):
        user.is_active = True

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def deactivate_user(self, user: User):
        print(user.is_active)
        user.is_active = False
        print(user.is_active)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_all_users(self) -> list[User] | None:
        return self.db.query(User).all()

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, id: int):
        return self.db.query(User).filter(User.id == id).first()

    def create_refresh_token(self, user: User, refresh_token: str, jti: str):
        token = RefreshToken(user_id=user.id, token=refresh_token, jti=jti)

        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)

        return token

    def get_refresh_token_by_jti(self, jti: str):
        return self.db.query(RefreshToken).filter(RefreshToken.jti == jti).first()

    def revoke_refresh_token(self, token: RefreshToken):
        token.is_revoked = True
        self.db.add(token)
        self.db.commit()

    def update_password(self, user: User, new_hash: str):
        user.password_hash = new_hash
        user.is_first_login = False

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
