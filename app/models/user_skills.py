import enum
from typing import Optional

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, ForeignKey, Enum

from app.db.base import Base, TimeStampMixin


class SkillLevel(enum.Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"


class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True
    )
    level: Mapped[Optional[SkillLevel]] = mapped_column(
        Enum(SkillLevel, name="skill_level_enum"), nullable=True
    )
