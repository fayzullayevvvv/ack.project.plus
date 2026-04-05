import enum
from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Enum

from app.db.base import Base


class RoleCode(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    worker = "worker"


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[RoleCode] = mapped_column(
        Enum(RoleCode, name="role_code"),
        unique=True,
        nullable=False,
        index=True,
    )

    users: Mapped[List["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles",
        lazy="selectin",
    )
