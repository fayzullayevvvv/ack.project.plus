from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    users: Mapped[list["UserSkill"]] = relationship("UserSkill", uselist=True, back_populates="skill")