from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean

from app.db.base import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["Profile"] = relationship("Profile", back_populates="user")
    roles: Mapped[list["UserRole"]] = relationship("UserRole", uselist=True, back_populates="user")
    skills: Mapped[list["UserSkill"]] = relationship("UserSkill", use_list=True, back_populates="user")