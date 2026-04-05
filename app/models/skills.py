from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)

    users: Mapped[List["User"]] = relationship(
        secondary="user_skills",
        back_populates="skills",
        lazy="selectin",
    )